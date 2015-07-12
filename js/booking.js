function addParamToBooking(content, type) {
	switch (type) {
		case "location":  // location
			booking.place = content;
			break;
		case "date":  // time
			booking.day = content;
			booking.month = (new Date()).getMonth()+1;
			booking.year = (new Date()).getFullYear();
			break;
		case "people":  // people
			booking.n_people = content;
			break;
		case "allergies":
			booking.allergies = content;
			break;
		case "menu":
			booking.menu_id = content;
			break;
		case "email":
			booking.email = content;
			break;
	}
}