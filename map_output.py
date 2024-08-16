import psycopg2
## if psycopg2 doesn't work, try 'pip install psycopg2-binary'
import folium
import psycopg2.extras
import db.SQLscripts as SQLscripts

def printd(message):
    """
    prints message
    """
    with open('logfile.txt', 'a') as f:
        f.write(str(message))

def run_map():
    # Initialize a map using folium at a default location
    m = folium.Map(location=[41.308964, -72.928531], zoom_start=18)

    # Loops through all roads with reports   
    all_roads = SQLscripts.all_roads()
    if all_roads is not None:
        for way in all_roads:
            location = way[0]
            avg_pass = way[1]
            current_color = get_color(avg_pass)
            if current_color is not None:
                        folium.GeoJson(
                            location,
                            style_function=lambda feature, color=current_color: {"color": color}
                        ).add_to(m)
    m.save('templates/map_display.html')

# Function to determine color based on passability, talk to Kevin about scores
def get_color(passability):
    if passability >= 90:
        return 'blue'
    elif passability >= 70:
        return 'red'
    elif passability >= 50:
        return 'orange'
    elif passability >= 10:
        return 'green'
    else:
        return None
    

def printd(message):
    """
    prints message
    """
    with open('logfile.txt', 'a') as f:
        f.write(str(message))
