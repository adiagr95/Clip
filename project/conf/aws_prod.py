AWS_STORAGE_BUCKET_NAME = 'prodstoragev4posoappcom'
AWS_ACCESS_KEY_ID = 'AKIAJ6BKLTL7OPIO2D7AA'
AWS_SECRET_ACCESS_KEY = 'd62MOumbvSL9u7h3yD8VDIxHEvy83Vdm92ec3c3c'

AWS_REGION = 'ap-southeast-1'
AWS_S3_HOST = 's3-%s.amazonaws.com' % AWS_REGION

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = 's3-%s.amazonaws.com/%s' % (AWS_REGION, AWS_STORAGE_BUCKET_NAME)

# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
