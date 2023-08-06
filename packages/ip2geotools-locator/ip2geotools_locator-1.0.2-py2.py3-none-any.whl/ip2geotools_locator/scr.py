from ip2geotools_locator import Locator

locator = Locator()

locator.get_locations("147.229.2.90", [])
#locator.get_locations("8.8.8.8", "*")

location = locator.calculate(median=True)

print(str(location))