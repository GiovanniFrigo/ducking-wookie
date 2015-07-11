function addParamToBooking(booking, param_i, content) {
	switch (param_i) {
		case 0:  // location
			booking.location = content;
			break;
		case 1:  // time
			booking.time = content;
			break;
		case 2:  // people
			booking.people = content;
			break;
		case 3:
			booking.allergies = content;
			break;
		case 4:
			booking.menu = content;
			break;
	}
}