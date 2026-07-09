from enum import Enum


class Department(str, Enum):
    ENGINEERING = "ENGINEERING"
    PRODUCT = "PRODUCT"
    DESIGN = "DESIGN"
    MARKETING = "MARKETING"
    SALES = "SALES"
    FINANCE = "FINANCE"
    OPERATIONS = "OPERATIONS"
    LEGAL = "LEGAL"


class SubDepartment(str, Enum):
    ENG_BACKEND = "ENG_BACKEND"
    ENG_FRONTEND = "ENG_FRONTEND"
    ENG_INFRA = "ENG_INFRA"
    ENG_DATA = "ENG_DATA"
    ENG_SECURITY = "ENG_SECURITY"
    PROD_MOBILE = "PROD_MOBILE"
    PROD_WEB = "PROD_WEB"
    PROD_GROWTH = "PROD_GROWTH"
    DES_UX = "DES_UX"
    DES_UI = "DES_UI"
    DES_RESEARCH = "DES_RESEARCH"
    MKT_CONTENT = "MKT_CONTENT"
    MKT_GROWTH = "MKT_GROWTH"
    MKT_BRAND = "MKT_BRAND"


class FilterStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    WITHDRAWN = "withdrawn"
    ALL = "all"
    WAITING_FOR_RECRUITER = "waiting_for_recruiter"
    WAITING_FOR_AI = "waiting_for_ai"
    WAITING_FOR_CANDIDATE = "waiting_for_candidate"
    ADVANCED = "advanced"
    DECLINED = "declined"


class UpdateActor(str, Enum):
    AI_AGENT = "ai_agent"
    HUMAN_RECRUITER = "human_recruiter"
    CANDIDATE = "candidate"


class UpdateType(str, Enum):
    RECOMMEND_ADVANCE = "recommend_advance"
    RECOMMEND_DECLINE = "recommend_decline"
    RECOMMEND_FOLLOW_UP = "recommend_follow_up"
    ADVANCE = "advance"
    DECLINE = "decline"
    FOLLOW_UP = "follow_up"
    REQUEST_AI_SCREEN = "request_ai_screen"
    GENERAL_UPDATE = "general_update"
    WITHDRAW = "withdraw"
