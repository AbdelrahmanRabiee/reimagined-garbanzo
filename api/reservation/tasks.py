from config.celery import app
from api.reservation.models import Reservation
from api.choices import ReservationStatus


@app.task(name='release_tickets')
def release_tickets(reservation_id):
    """get reservation object and change the status to FAILD only if the status is PROCESSING"""
    reservation = Reservation.objects.filter(id=reservation_id)
    if reservation.exists() and reservation.first().status != ReservationStatus.PAID:
        reservation = reservation.first()
        if reservation.status != ReservationStatus.PAID:
            reservation.status = ReservationStatus.FAILED
            reservation.save()
