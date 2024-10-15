
# Maximum length for names of all kinds
MAX_USER_NAMES_L = 150

# Maximum length for emails
MAX_EMAIL_L = 254

# Maximum role length
MAX_ROLE_L = 16

# Maximum code length
MAX_CODE_L = 4

# Maximum token length
MAX_TOKEN_L = 255

# Admin role
ADMIN = "admin"

# Moderator role
MODERATOR = "moderator"

# User role
USER = "user"

# User roles
CHOICES = (
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
)

PATTERN = r"^[\w.@+-]+\Z"
