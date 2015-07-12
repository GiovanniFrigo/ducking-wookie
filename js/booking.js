function addParamToBooking(content, type) {
	switch (type) {
		case "location":  // location
			booking.location = content;
			break;
		case "time":  // time
			booking.time = content;
			break;
		case "people":  // people
			booking.people = content;
			break;
		case "allergies":
			booking.allergies = content;
			break;
		case "menu":
			booking.menu = content;
			break;
	}
}