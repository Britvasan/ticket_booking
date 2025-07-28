app_name = "cinema"
app_title = "Cinema"
app_publisher = "Brit"
app_description = "Cinema"
app_email = "britvasan12@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "cinema",
# 		"logo": "/assets/cinema/logo.png",
# 		"title": "Cinema",
# 		"route": "/cinema",
# 		"has_permission": "cinema.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/cinema/css/cinema.css"
# app_include_js = "/assets/cinema/js/cinema.js"



# include js, css files in header of web template
# web_include_css = "/assets/cinema/css/cinema.css"

# Movies page css

# web_include_css = "/assets/cinema/css/movies.css"
# web_include_js = "/assets/cinema/js/cinema.js"



# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "cinema/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}




# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "cinema/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "cinema.utils.jinja_methods",
# 	"filters": "cinema.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "cinema.install.before_install"
# after_install = "cinema.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "cinema.uninstall.before_uninstall"
# after_uninstall = "cinema.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "cinema.utils.before_app_install"
# after_app_install = "cinema.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "cinema.utils.before_app_uninstall"
# after_app_uninstall = "cinema.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "cinema.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"cinema.tasks.all"
# 	],
# 	"daily": [
# 		"cinema.tasks.daily"
# 	],
# 	"hourly": [
# 		"cinema.tasks.hourly"
# 	],
# 	"weekly": [
# 		"cinema.tasks.weekly"
# 	],
# 	"monthly": [
# 		"cinema.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "cinema.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "cinema.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "cinema.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["cinema.utils.before_request"]
# after_request = ["cinema.utils.after_request"]

# Job Events
# ----------
# before_job = ["cinema.utils.before_job"]
# after_job = ["cinema.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"cinema.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

doc_events = {
    "Booking": {
        "validate": "cinema.cinema.booking_logic.validate_seats",
        "on_submit": "cinema.cinema.booking_logic.on_submit_generate_qr",
        "after_insert": "cinema.booking_chart.after_insert"
    },
    "Theatre": {
        "before_save": "cinema.cinema.doctype.theatre.theatre.update_screen_capacities"
    }
}


website_route_rules = [
    {"from_route": "/", "to_route": "home"},
    {"from_route": "/movies", "to_route": "movies"},
    {"from_route": "/movie/<movie_name>", "to_route": "movie_detail"},
    {"from_route": "/book/<showtime_id>", "to_route": "book"},
    {"from_route": "/ticket/<booking_id>", "to_route": "ticket_view"}
]

email_templates = [
    "cinema/templates/emails/booking_ticket_email.html"
]

scheduler_events = {
    "cron": {
        "*/5 * * * *": [
            "cinema.api.scheduler.send_showtime_reminders"
        ]
    }
}


doctype_list_js = {
    "QR Scan Log": "public/js/qr_log.js"
}


app_include_js = [
    "https://checkout.razorpay.com/v1/checkout.js"
]


website_context = {
    "favicon": "/assets/cinema/images/clapperboard.png",
    "brand_html": "<b>Book Your Show</b>"
}

ignore_links_on_delete = ["Booking", "Showtime", "Theatre", "Customer"]

# app_include_js = "/assets/cinema/js/desk_custom.js"
# app_include_css = "/assets/cinema/css/desk_theme.css"

# website_context = {
#     "brand_html": '<img src="/assets/cinema/images/clapperboard.png" height="30">'
# }

# website_redirects = [
#     {"source": "/movie", "target": "/movies"},
#     # {"source": r"/movie(/.*)?", "target": "/movies\\1"}
# ]

# website_path_resolver = "cinema.path_resolver.resolve"

# homepage = "home"

# Permissions

# permission_query_conditions = {
#     "Booking": "cinema.permissions.booking_info"
# }

