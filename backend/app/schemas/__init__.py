from .auth import SignupRequest, LoginRequest, AuthResponse, UserResponse
from .warranty import WarrantyCreate, WarrantyUpdate, WarrantyResponse, WarrantyListResponse
from .product import ProductCreate, ProductUpdate, ProductResponse
from .category import CategoryCreate, CategoryResponse
from .notification import NotificationResponse
from .chat import ChatMessageCreate, ChatMessageResponse, ChatSessionResponse

# Re-export all schemas
__all__ = [
    # Auth
    'SignupRequest',
    'LoginRequest',
    'AuthResponse',
    'UserResponse',
    
    # Warranty
    'WarrantyCreate',
    'WarrantyUpdate',
    'WarrantyResponse',
    'WarrantyListResponse',
    
    # Product
    'ProductCreate',
    'ProductUpdate',
    'ProductResponse',
    
    # Category
    'CategoryCreate',
    'CategoryResponse',
    
    # Notification
    'NotificationResponse',
    
    # Chat
    'ChatMessageCreate',
    'ChatMessageResponse',
    'ChatSessionResponse',
]
