from __future__ import print_function
import csv

class Map(object):
    def __init__(self):
        self._points = []
    def add_point(self, coordinates):
        self._points.append(coordinates)
    def __str__(self):
        centerLat = sum(( x[0] for x in self._points )) / len(self._points)
        centerLon = sum(( x[1] for x in self._points )) / len(self._points)
        markersCode = "\n".join(
            [ """
              var drone = {
              path: 'M -15 -30 a 15 15 0 1 0 0.001 0 M -15 0 a 15 15 0 1 0 0.001 0 M 15 -30 a 15 15 0 1 0 0.001 0 M 15 0 a 15 15 0 1 0 0.001 0 M -15 -16 a 2 2 0 1 0 0.001 0 M -15 14 a 2 2 0 1 0 0.001 0  M 15 -16 a 2 2 0 1 0 0.001 0 M 15 14 a 2 2 0 1 0 0.001 0 M 0 -8 a 8 8 0 1 0 0.001 0 M 0 -6 a 6 6 0 1 0 0.001 0 M 0 -4 a 4 4 0 1 0 0.001 0 M 0 -2 a 2 2 0 1 0 0.001 0',
              fillColor: 'white',
              fillOpacity: 0.9,
              scale: 0.9,
              strokeColor: 'black',
              strokeWeight: 3
              };

              var marker = new google.maps.Marker({
              position: map.getCenter(),
              icon: drone,
              map: map
              }); 
              """
            ])
        flightCode = "\n".join(
            [ """
              var flightPlanCoordinates = [
                {lat: 39.797400, lng: -104.925723},
                {lat: 39.736504, lng: -105.000497},
              ];
        
              var flightPath = new google.maps.Polyline({
              path: flightPlanCoordinates,
              geodesic: true,
              strokeColor: '#00FF00',
              strokeOpacity: 0.5,
              strokeWeight: 8
              });

              flightPath.setMap(map);
              """
            ])
        circleCode = "\n".join(
            [ """
              var circlemap = {
                 c190: {center: {lat: 39.731245, lng: -105.011729}, radius: 46},
                 c99:  {center: {lat: 39.729041, lng: -105.009604}, radius: 305},
                 c189: {center: {lat: 39.735067, lng: -105.005585}, radius: 30},
                 c112: {center: {lat: 39.742136, lng: -104.996824}, radius: 203},
                 c15:  {center: {lat: 39.746883, lng: -104.991230}, radius: 76},
                 c1:   {center: {lat: 39.747704, lng: -104.989786}, radius: 73},
                 c51:  {center: {lat: 39.749525, lng: -104.989296}, radius: 76},
                 c188: {center: {lat: 39.758223, lng: -104.976227}, radius: 61},
                 c183: {center: {lat: 39.762682, lng: -104.971722}, radius: 76},
                 c117: {center: {lat: 39.762538, lng: -104.969226}, radius: 76},
                 c120: {center: {lat: 39.771979, lng: -104.951384}, radius: 91},
                 c185: {center: {lat: 39.768783, lng: -104.958465}, radius: 61},
                 c173: {center: {lat: 39.766384, lng: -104.967888}, radius: 76},
                 c157: {center: {lat: 39.767465, lng: -104.967830}, radius: 46},
                 c177: {center: {lat: 39.768225, lng: -104.968306}, radius: 30},
                 c182: {center: {lat: 39.766362, lng: -104.970360}, radius: 46},
                 c187: {center: {lat: 39.755705, lng: -104.983248}, radius: 46},
                 c4:   {center: {lat: 39.747638, lng: -104.987722}, radius: 76},
                 c27:  {center: {lat: 39.747768, lng: -104.986420}, radius: 76},
                 c5:   {center: {lat: 39.747114, lng: -104.990486}, radius: 76},
                 c28:  {center: {lat: 39.746145, lng: -104.991462}, radius: 76},
                 c46:  {center: {lat: 39.745827, lng: -104.992438}, radius: 73},
                 c25:  {center: {lat: 39.745302, lng: -104.990808}, radius: 76},
                 c20:  {center: {lat: 39.746075, lng: -104.989914}, radius: 76},
                 c11:  {center: {lat: 39.746578, lng: -104.989988}, radius: 76},
                 c7:   {center: {lat: 39.743472, lng: -104.993590}, radius: 73},
                 c113: {center: {lat: 39.743503, lng: -104.990960}, radius: 107},
                 c53:  {center: {lat: 39.744141, lng: -104.994851}, radius: 76},
                 c63:  {center: {lat: 39.740330, lng: -104.991959}, radius: 76},
                 c8:   {center: {lat: 39.744827, lng: -104.995607}, radius: 76},
                 c18:  {center: {lat: 39.747645, lng: -104.993750}, radius: 76},
                 c35:  {center: {lat: 39.748168, lng: -104.993605}, radius: 76},
                 c37:  {center: {lat: 39.748255, lng: -104.994074}, radius: 76},
                 c116: {center: {lat: 39.748019, lng: -104.994604}, radius: 61},
                 c16:  {center: {lat: 39.749595, lng: -104.992569}, radius: 76},
                 c17:  {center: {lat: 39.749998, lng: -104.991988}, radius: 76},
                 c169: {center: {lat: 39.749318, lng: -104.990936}, radius: 30},
                 c45:  {center: {lat: 39.749235, lng: -104.991325}, radius: 76},
                 c111: {center: {lat: 39.744706, lng: -104.997977}, radius: 183},
                 c92:  {center: {lat: 39.739237, lng: -104.994789}, radius: 76},
                 c93:  {center: {lat: 39.739304, lng: -104.993459}, radius: 76},
                 c94:  {center: {lat: 39.739214, lng: -104.992260}, radius: 76},
                 c90:  {center: {lat: 39.739243, lng: -104.990970}, radius: 76},
                 c102: {center: {lat: 39.737313, lng: -104.992190}, radius: 305},
                 c107: {center: {lat: 39.743794, lng: -105.020018}, radius: 457},
                 c18:  {center: {lat: 39.747645, lng: -104.993750}, radius: 76},
                 c39:  {center: {lat: 39.745173, lng: -104.996186}, radius: 76},
                 c22:  {center: {lat: 39.748099, lng: -104.995687}, radius: 76},
                 c12:  {center: {lat: 39.746328, lng: -104.996784}, radius: 76},
                 c58:  {center: {lat: 39.741574, lng: -104.992880}, radius: 76},
                 c77:  {center: {lat: 39.742318, lng: -104.991880}, radius: 76},
                 c150: {center: {lat: 39.768890, lng: -104.949390}, radius: 46},
                 c170: {center: {lat: 39.762956, lng: -104.971523}, radius: 46},
                 c119: {center: {lat: 39.756189, lng: -104.967788}, radius: 152},
                 c186: {center: {lat: 39.759616, lng: -104.978212}, radius: 30},
                 c179: {center: {lat: 39.752690, lng: -104.972748}, radius: 76},
                 c67:  {center: {lat: 39.747906, lng: -104.979550}, radius: 76},
                 c36:  {center: {lat: 39.745761, lng: -104.988832}, radius: 76},
                 c6:   {center: {lat: 39.745354, lng: -104.989356}, radius: 76},
                 c47:  {center: {lat: 39.744781, lng: -104.989742}, radius: 76},
                 c19:  {center: {lat: 39.743942, lng: -104.989726}, radius: 76},
                 c34:  {center: {lat: 39.744050, lng: -104.988933}, radius: 76},
                 c49:  {center: {lat: 39.744425, lng: -104.988327}, radius: 76},
                 c61:  {center: {lat: 39.744930, lng: -104.987839}, radius: 76},
                 c0:   {center: {lat: 39.743526, lng: -104.987650}, radius: 76},
                 c43:  {center: {lat: 39.743588, lng: -104.986928}, radius: 76},
                 c33:  {center: {lat: 39.742750, lng: -104.987843}, radius: 76},
                 c9:   {center: {lat: 39.742924, lng: -104.986752}, radius: 76},
                 c23:  {center: {lat: 39.742930, lng: -104.985736}, radius: 76},
                 c2:   {center: {lat: 39.743633, lng: -104.985467}, radius: 76},
                 c21:  {center: {lat: 39.744567, lng: -104.985242}, radius: 76},
                 c118: {center: {lat: 39.745592, lng: -104.985712}, radius: 61},
                 c42:  {center: {lat: 39.741903, lng: -104.989168}, radius: 76},
                 c87:  {center: {lat: 39.740830, lng: -104.990030}, radius: 76},
                 cSw:  {center: {lat: 39.781247, lng: -104.956610}, radius: 76},
                 cCF:  {center: {lat: 39.756177, lng: -104.994198}, radius: 200},
              };
        
              for (var circ in circlemap) {
                var cityCircle = new google.maps.Circle({
                  strokeColor: '#FF0000',
                  strokeOpacity: 0.8,
                  strokeWeight: 4,
                  fillColor: '#FF0000',
                  fillOpacity: 0.20,
                  map: map,
                  center: circlemap[circ].center,
                  radius: circlemap[circ].radius
                });
              }
              """
            ])
        smflightCode = "\n".join(
            [ """
              var flightPlanCoordinates = [
                {lat: 39.736504, lng: -105.000497},
                {lat: 39.740564, lng: -104.995215},
                {lat: 39.740731, lng: -104.995022},
                {lat: 39.742851, lng: -104.992856},
                {lat: 39.742908, lng: -104.992803},
                {lat: 39.742969, lng: -104.992755},
                {lat: 39.743035, lng: -104.992712},
                {lat: 39.743103, lng: -104.992675},
                {lat: 39.743175, lng: -104.992645},
                {lat: 39.743249, lng: -104.992621},
                {lat: 39.743325, lng: -104.992603},
                {lat: 39.743402, lng: -104.992592},
                {lat: 39.743479, lng: -104.992588},
                {lat: 39.743557, lng: -104.992590},
                {lat: 39.743634, lng: -104.992600},
                {lat: 39.743711, lng: -104.992616},
                {lat: 39.743856, lng: -104.992667},
                {lat: 39.745460, lng: -104.993391},
                {lat: 39.745532, lng: -104.993420},
                {lat: 39.745607, lng: -104.993442},
                {lat: 39.745683, lng: -104.993458},
                {lat: 39.745760, lng: -104.993467},
                {lat: 39.745838, lng: -104.993470},
                {lat: 39.745916, lng: -104.993465},
                {lat: 39.745993, lng: -104.993454},
                {lat: 39.746069, lng: -104.993437},
                {lat: 39.746142, lng: -104.993412},
                {lat: 39.746214, lng: -104.993382},
                {lat: 39.746283, lng: -104.993345},
                {lat: 39.746348, lng: -104.993302},
                {lat: 39.746409, lng: -104.993254},
                {lat: 39.746466, lng: -104.993201},
                {lat: 39.746530, lng: -104.993128},
                {lat: 39.747585, lng: -104.991781},
                {lat: 39.747658, lng: -104.991671},
                {lat: 39.748481, lng: -104.990224},
                {lat: 39.748516, lng: -104.990154},
                {lat: 39.748545, lng: -104.990082},
                {lat: 39.748568, lng: -104.990008},
                {lat: 39.748584, lng: -104.989931},
                {lat: 39.748594, lng: -104.989846},
                {lat: 39.748635, lng: -104.989236},
                {lat: 39.748643, lng: -104.989159},
                {lat: 39.748658, lng: -104.989083},
                {lat: 39.748680, lng: -104.989008},
                {lat: 39.748709, lng: -104.988935},
                {lat: 39.748743, lng: -104.988866},
                {lat: 39.748783, lng: -104.988799},
                {lat: 39.748836, lng: -104.988728},
                {lat: 39.758774, lng: -104.976681},
                {lat: 39.758840, lng: -104.976586},
                {lat: 39.761910, lng: -104.971275},
                {lat: 39.761952, lng: -104.971209},
                {lat: 39.762020, lng: -104.971124},
                {lat: 39.763199, lng: -104.969825},
                {lat: 39.763243, lng: -104.969773},
                {lat: 39.797400, lng: -104.925723},
              ];
        
              var flightPath = new google.maps.Polyline({
              path: flightPlanCoordinates,
              geodesic: true,
              strokeColor: '#0000FF',
              strokeOpacity: 0.5,
              strokeWeight: 8
              });

              flightPath.setMap(map);
              """
            ])
        return """
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
            <div id="map-canvas" style="height: 100%; width: 100%"></div>
            <script type="text/javascript">
                var map;
                function show_map() {{
                    map = new google.maps.Map(document.getElementById("map-canvas"), {{
                        zoom: 17,
                        center: new google.maps.LatLng({centerLat}, {centerLon}),
                        mapTypeId: google.maps.MapTypeId.HYBRID
                    }});
                    {markersCode}
                    {flightCode}
                    {circleCode}
                    {smflightCode}
                }}
                google.maps.event.addDomListener(window, 'load', show_map);
            </script>
        """.format(centerLat=centerLat, centerLon=centerLon,
                   markersCode = markersCode, flightCode = flightCode, 
                   circleCode = circleCode, smflightCode = smflightCode)

def load_file(fname):
    ''' loads a csv file '''
    lst = []
    with open(fname,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            lst.append((float(row[0]), float(row[1])))
    return lst

def load_count(fname):
    ''' loads the count '''
    lst = [] 
    with open(fname,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            lst.append(row)
    return int(lst[0][0])

def export_count(fname, cnt):
    ''' exports an incremented count'''
    out = csv.writer(open(fname,"w"), delimiter=',', \
                     quoting=csv.QUOTE_MINIMAL)
    out.writerow([cnt])
 

if __name__ == "__main__":
        path = load_file('path_detailed.csv')
        cnt = load_count('p_count.csv')
        lat = path[cnt][1]
        lng = path[cnt][0]
        cnt -= 1
        export_count('p_count.csv', cnt)
        map = Map()
        map.add_point((lat, lng))
        with open("output.html", "w") as out:
            print(map, file=out)
