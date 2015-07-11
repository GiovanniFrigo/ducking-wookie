function addParamToBooking(booking, param_i, content) {
	switch (param_i) {
		case 0:  // location
			booking.location = content;
			break;
		case 1:  // time
			booking.time = content;
			break;
	}
}