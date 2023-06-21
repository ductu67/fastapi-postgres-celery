class Route:
    class V1:
        API = "api"
        VERSION = "v1"
        prefix_api = "/" + API + "/" + VERSION

        # HEALTHCHECK
        HEALTH_CHECK = "/"

        #         Auth
        LOGIN = "/login"
        REGISTER = "/register"

        #         Project
        GET_LIST_PROJECT = "/project"
        CREATE_PROJECT = "/project"
        UPDATE_PROJECT = "/project"
        GET_PROJECT_DETAIL = "/project/{project_id}"

        #       Notification
        GET_NOTIFICATION_BY_ID = '/notification/{user_id}'
        REGISTER_FCM_DEVICE = '/notification/fcm-device'
        TEST_FUNCTION = '/notification/test-noti'
        EMAIL = '/test-email'
