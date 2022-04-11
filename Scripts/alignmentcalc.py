import math

class alignmentcalc:
   # movable-type.co.uk/scripts/latlong.html
   def getAngle(lat1, lon1, lat2, lon2):
      deltaLon = (lon2 - lon1)
      y = math.sin(deltaLon) * math.cos(lat2)
      x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(deltaLon)
      bearing = math.atan2(y, x)
      bearing = math.degrees(bearing)
      bearing = (bearing + 360) % 360

      bearing = 360 - bearing #count degrees counter-clockwise - remove to make clockwise

      return bearing

   # refer to haversine formula on wikipedia
   def distanceBetween(lat1, lon1, lat2, lon2):
      deltaLon = (lon2 - lon1) / 2
      deltaLat = (lat2 - lat1) / 2
      distance = 2 * 6378.1370 * 1000 * math.radians(math.asin(math.sqrt(math.pow(math.sin(deltaLat), 2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(deltaLon), 2))))

      return distance

