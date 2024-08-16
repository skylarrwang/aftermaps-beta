"""
Middle layer for Aftermaps
"""
import db.SQLscripts as SQLscripts
import mysql.connector as sqlpck
import re
import time
from helpers.app_helpers import login_required
from helpers.map_helper import lat_long_validation
from helpers.output_helper import format_home
from flask import Flask, request, render_template, session, flash, redirect
from flask_session import Session
from werkzeug.security import check_password_hash
from helpers.geocode_helper import haversine, get_longitude_latitude
from re import match
from submitreport import report_controller
from map_output import run_map
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False

### We may want to switch this to signed cookies in the long run
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def printd(message):
    """
    prints message
    """
    with open('logfile.txt', 'a') as f:
        f.write(str(message))

@app.route('/', methods=["GET"])
def homepage():
    return render_template("login.html")

@app.route('/report', methods=["GET", "POST"])
@login_required
def report():
    if request.method == "POST":
        return handle_map_submission(request)
    else:    
        return render_template("report.html")

def handle_map_submission(request):
    ## This returns the lat and long
    curr_lat = request.form.get("latitude")
    curr_long = request.form.get("longitude")
    rep_lat = request.form.get("rLatitude")
    rep_long = request.form.get("rLongitude")
    passability = request.form.get("passability")
    
    printd(f"curr coord is: {curr_lat},{curr_long} \n report coord: {rep_lat}, {rep_long} \n passability: {passability}")
    
    ## validate input
    flash_message = lat_long_validation(curr_lat, curr_long, rep_lat, rep_long)
    if flash_message:
        flash(flash_message)
        return render_template("report.html")
    
    ## calculate distance
    report_distance = haversine(float(curr_long), float(curr_lat), 
                float(rep_long), float(rep_lat))
    
    ## find the closest way
    printd(f"lat and long are: {rep_lat}, {rep_long}")
    row = SQLscripts.closest_road(rep_long, rep_lat)
    if row:
        road_id = row[0]
        way_distance = row[1]
        printd(f"DISTANCE IS: {way_distance}")
        
        ## check that it corresponds with the ways we have logged
        if int(way_distance) > 20:
            flash("Point too far from logged ways (only have testing in New Haven right now)")
            return render_template("report.html")
    else:
        flash("Couldn't retrieve corresponding way :(")
        return render_template("report.html")
     
    ## pass into SQL controller
    userID = str(session["user_id"])
    report_controller(userID, road_id, curr_long, curr_lat, rep_long, rep_lat, report_distance, passability)
    
    ## Flash successful report
    flash("Report submitted successfully.")
    return render_template("report.html")


@app.route('/map', methods=["GET"])
def map():
    run_map()
    format_home()
    return render_template("map_home.html")

LOCKOUT_THRESHOLD = 3  # Number of consecutive failed login attempts before lockout
LOCKOUT_DURATION = 300  # Lockout duration in seconds (5 minutes)

# Dictionary to store failed login attempts and lockout time
failed_login_attempts = {}

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via form submission
    if request.method == "POST":

        # Handle username/pwd submissions
        if not request.form.get("username"):
            flash("Must provide username")
            return render_template("login.html")
        elif not request.form.get("password"):
            flash("Must provide password")
            return render_template("login.html")

        # Check if the user is currently locked out
        username = request.form.get("username")
        if username in failed_login_attempts:
            lockout_time = failed_login_attempts[username]
            if time.time() - lockout_time < LOCKOUT_DURATION:
                remaining_time = int(LOCKOUT_DURATION - (time.time() - lockout_time))
                flash(f"Account locked. Please try again after {remaining_time} seconds.")
                return render_template("login.html")

        # Query database for username
        rows = SQLscripts.login_query(username)
        
        # Ensure username exists and password is correct
        if rows is None or not check_password_hash(rows[1], request.form.get("password")):
            # Increment failed login attempts count
            failed_login_attempts[username] = failed_login_attempts.get(username, 0) + 1
            # Check if lockout threshold reached
            if failed_login_attempts[username] >= LOCKOUT_THRESHOLD:
                failed_login_attempts[username] = time.time()  # Record lockout time
                flash("Too many failed login attempts. Account locked for 5 minutes.")
            else:
                flash("Username or password incorrect")
            return render_template("login.html")

        # Clear failed login attempts upon successful login
        failed_login_attempts.pop(username, None)

        # Remember which user has logged in
        session["user_id"] = rows[0]
        return redirect("/report")

    # User reached route via GET
    else:
        return render_template("login.html")

@app.route("/logout", methods=["GET"])
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username")
            return render_template("register.html")

        # Ensure password was submitted
        if not request.form.get("password"):
            flash("Must provide password")
            return render_template("register.html")

        # Ensure password confirmation was submitted
        if not request.form.get("confirmation"):
            flash("Must retype password to confirm")
            return render_template("register.html")
        
        # Ensure password was typed in correctly both times
        if request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords do not match")
            return render_template("register.html")

        # Ensure password meets criteria
        password = request.form.get("password")
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$", password):
            flash("Password must be at least 8 characters, including uppercase, lowercase, a number, and a special character")
            return render_template("register.html")

        # Check if username already exists
        rows = SQLscripts.login_query(request.form.get("username"))
        if rows:
            flash("Username taken, please choose a new one")
            return render_template("register.html")
        
        # Register user
        try:
            SQLscripts.register_user(request.form.get("username"), request.form.get("password"))
            return redirect("/")
        except sqlpck.Error as error:
            # Handle MySQL errors
            flash("An error occurred while registering the user")
            print(f"MySQL Error: {error}")
            return render_template("register.html")
        except Exception as e:
            # Handle other unexpected exceptions
            flash("An unexpected error occurred")
            print(f"Unexpected Error: {e}")
            return render_template("register.html")

    # User reached route via GET
    else:
        return render_template("register.html")

def handle_report_submission(request):
    ## get inputs
    address = request.form.get("address")
    city = request.form.get("city")
    state = request.form.get("state")
    zip = request.form.get("zip")
    passability = request.form.get("passability")
    curr_long = request.form.get("longitude")
    curr_lat = request.form.get("latitude")
    full_address = f"{address}, {city}, {state}, {zip}"
    
    ## validate input
    flash_message = input_validation(curr_long, curr_lat, address, city, state, zip)
    if flash_message:
        flash(flash_message)
        return render_template("report.html")
    
    ## calculate distance 
    distance, add_long, add_lat = get_distance(full_address, curr_long, curr_lat)
    if distance is None:
        flash("Error: could not retrieve address") 
        return render_template("report.html")
    
    ## pass into SQL controller
    userID = str(session["user_id"])
    report_controller(userID, full_address, curr_long, curr_lat, add_long, add_lat, distance, passability)
    
    ## Flash successful report
    flash("Report submitted successfully.")
    return render_template("report.html")


def input_validation(curr_long, curr_lat, address, city, 
                     state, zip):
    ## Check location is enabled
    if curr_long == "" or curr_lat == "":
        return "Error: Please enable location tracking."
    
    ## Check source is fully inputted
    if not address or not city or not state or not zip:
        return "Error: missing input field."
    
    ## Check address formatting
    if not match(r'^\d+\s[A-Za-z]+\s[A-Za-z]*', address):
        return "Error: Please enter a valid address format (e.g., 123 Main St)."
    
    ## Check zip formatting
    if not zip.isdigit() or len(zip) != 5:
        return "Error: Please enter a valid 5-digit zip code."
        
    return None  # Return None if no flash message is generated

def get_distance(full_address, curr_long, curr_lat):
    try:
        (add_long, add_lat) = get_longitude_latitude(full_address)
        distance = haversine(float(curr_long), float(curr_lat), 
                        float(add_long), float(add_lat))
    except:
        distance is None
    return distance, add_long, add_long