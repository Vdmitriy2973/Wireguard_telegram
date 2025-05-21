from aiogram import Router

from .buy_vpn_config import router as vpn_price_list_router
from .renew_vpn_config import router as extend_config_router
from .get_vpn_service_info import router as my_services_router
from .get_vpn_subscription import router as buy_vpn_services_router
from .success_payments_handlers import router as payment_router
from .start_command import router as start_router
from .cancel_vpn_config import cancel_router
from .connection_guide import router_guide

main_router = Router()
main_router.include_router(my_services_router)
main_router.include_router(cancel_router)
main_router.include_router(router_guide)
main_router.include_router(buy_vpn_services_router)
main_router.include_router(start_router)
main_router.include_router(vpn_price_list_router)
main_router.include_router(extend_config_router)
main_router.include_router(payment_router)
