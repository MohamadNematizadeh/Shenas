from fastapi import FastAPI, UploadFile, HTTPException, Depends
from celery_tasks import celery_app, face_task, speech_task, gesture_task
from users import (
    SignUpRequest,
    SignInRequest,
    TokenResponse,
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)
from database import User

app = FastAPI()

@app.post("/signup", status_code=201)
def signup(request: SignUpRequest):
    if User.objects(email=request.email).first():
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_password = get_password_hash(request.password)
    User(email=request.email, hashed_password=hashed_password, level=1).save()
    return {"message": "User registered successfully."}

@app.post("/signin", response_model=TokenResponse)
def signin(request: SignInRequest):
    user = User.objects(email=request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    access_token = create_access_token(data={"email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/profile")
def profile(current_user: str = Depends(get_current_user)):
    user = User.objects(email=current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return {"email": user.email, "message": "This is your profile."}

@app.post("/auth/face")
async def auth_face(file: UploadFile, current_user: str = Depends(get_current_user)):
    task = face_task.delay(await file.read())
    return {"task_id": task.id, "status": "processing"}

@app.post("/auth/speech")
async def auth_speech(file: UploadFile, current_user: str = Depends(get_current_user)):
    task = speech_task.delay(await file.read())
    return {"task_id": task.id, "status": "processing"}

@app.post("/auth/gesture")
async def auth_gesture(file: UploadFile, current_user: str = Depends(get_current_user)):
    task = gesture_task.delay(await file.read())
    return {"task_id": task.id, "status": "processing"}

@app.get("/task_status/{task_id}")
def get_task_status(task_id: str, current_user: str = Depends(get_current_user)):
    result = celery_app.AsyncResult(task_id)
    if result.state == "PENDING":
        return {"status": "pending"}
    elif result.state == "SUCCESS":
        return {"status": "completed", "result": result.result}
    else:
        return {"status": "failed"}
