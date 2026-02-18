from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware
from database.db import init_db
from routes import register,login, add_product, order
from fastapi.staticfiles import StaticFiles



app = FastAPI(
    title="Book Store API",
    version="1.0.0",
    openapi_version="3.0.3",
    docs_url="/api/docs",           # Swagger UI
    redoc_url="/api/redoc",         # ReDoc
    openapi_url="/api/openapi.json" # OpenAPI schema
)

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# CORS (React support)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(register.router, prefix="/api")
app.include_router(login.router, prefix="/api")
app.include_router(add_product.router, prefix="/api")
app.include_router(order.router, prefix="/api")

# Startup event → create tables
@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def root():
    return {"message": "Book Store API Running 🚀"}


