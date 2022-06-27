from rest_framework import mixins, viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from api.reservation.models import Reservation
from api.choices import ReservationStatus
from api.reservation.serializers import ReservationCreateSerializer, ReservationListSerializer
from api.reservation.payment_gateway import PaymentGateway, CardError, CurrencyError, PaymentError


class ReservationsViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    serializer_classes = {
        'create': ReservationCreateSerializer,
        'list': ReservationListSerializer,
        'retrieve': ReservationListSerializer
    }
    queryset = Reservation.objects.all().prefetch_related('tickets')
    permission_classes = (AllowAny,)
    lookup_field = 'id'

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)

    @action(detail=True)
    def pay(self, request, *args, **kwargs):
        """change status of reservation to PAID if payment is successful"""
        reservation = self.get_object()
        token = '####dummy#token#####'
        if reservation.status != ReservationStatus.PROCESSING:
            token = 'payment_error'
        try:
            payment = PaymentGateway()
            result = payment.charge(reservation.total_price, token)
            reservation.status = ReservationStatus.PAID
            reservation.save()
            return_data = {'status': ReservationStatus.PAID, 'result': result}
            return Response(data=return_data,
                            status=status.HTTP_200_OK)
        except CardError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except CurrencyError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        except PaymentError as e:
            return Response(data={'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
