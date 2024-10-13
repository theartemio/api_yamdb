
# Maximum length for names of all kinds
MAX_USER_NAMES_L = 150

# Maximum length for emails
MAX_EMAIL_L = 254

# Maximum role length
MAX_ROLE_L = 16

# User roles
CHOICES = (
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
)

PATTERN = r"^[\w.@+-]+\Z"
