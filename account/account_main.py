# -*- coding:utf-8 -*-
import logging
import requests
from flask import Blueprint
from svc_util import log_control

activity_console = Blueprint('activity_console', __name__)


def init_each_process():
    """
    子进程自己初始化句柄，避免从主进程继承
    :return:
    """
    log_control.get_log(None, url_hosts.LOG_SET, logging.INFO if url_hosts.ENV == 'release' else logging.DEBUG)


class Account(object):
    """
    主进程的所有东西都会被子进程继承，尽量不要初始化太多东西
    """

    @classmethod
    def setup(cls, app):
        svc_utils.get_log(None, url_hosts.LOG_SET, logging.INFO if url_hosts.ENV == 'release' else logging.DEBUG)
        logging.info('wsgi application[%s] setup' % url_hosts.APP_NAME)

        app.before_first_request(init_each_process)

        # 改变requests的特性
        requests.adapters.DEFAULT_RETRIES = 1
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        Content.add_urls(activity_console)
        app.register_blueprint(activity_console, url_prefix='/activity_console')

    @classmethod
    def add_urls(cls, blue):
        activity = Activity()
        dynamic_block = DynamicBlock()
        product = Product()
        goods = Goods()
        api_tof = Api_tof()
        blacklist = BlackList()
        activity_category = ActivityCategory()
        goods_pacakge = GoodsPackage()
        voucher = Voucher()
        goods_discount = GoodsDiscount()
        activity_stat = ActivityStat()

        goods_approval = GoodsApproval()
        activity_approval = ActivityApproval()
        approval = Approval()
        test_white_list = TestWhiteList()
        from_generator = FromGenerator()
        api_goods_config = Api_goods_config()
        alert = Alert()
        voucher_tools = VoucherTools()
        strategy = ActivityRestrictStrategy()

        exclusive_package = UserExclusivePackage()
        exclusive_package_approval = UserExclusivePackageApproval()

        score_convert = ScoreConvert()
        activity_secret = ActivitySecret()
        comm_form = CommForm()
        m_template_page = Api_template_page()


        post_urls = {
            '/activity/list_id_name': activity.list_id_name,
            '/activity/list': activity.list,
            '/activity/add': activity.add,
            '/activity/add_inner': activity.add_inner,
            '/activity/remove': activity.remove,
            '/activity/update': activity.update,
            '/activity/query': activity.query,
            '/activity/check_activity_permission': activity.check_activity_permission,
            '/activity/sync_create_trade_activity': activity.sync_create_trade_activity,
            '/activity/stat': activity.stat,
            '/activity/stat_list': activity.stat_list,
            '/activity/ft': activity.query_ft,
            '/activity/activity_check': activity.activity_check,
            '/activity/check_activity_id': activity.check_activity_id,
            '/activity/get_activity_properties': activity.get_activity_properties,
            '/activity/get_activity_product_table_info': activity.get_activity_product_table_info,
            '/activity/get_user_roles': activity.get_user_roles,

            '/activity/strategy_add': strategy.activity_restrict_strategy_add,
            '/activity/strategy_switch': strategy.activity_restrict_strategy_switch,
            '/activity/strategy_update': strategy.activity_restrict_strategy_update,
            '/activity/strategy_list': strategy.activity_restrict_strategy_list,

            '/activity/query_secret': activity_secret.query_secret,
            '/activity/gen_secret': activity_secret.gen_secret,
            '/activity/list_secret': activity_secret.list_secret,

            '/activity/get_user_condition_logs': activity.get_user_condition_logs,

            '/dynamic_block/list': dynamic_block.list,
            '/dynamic_block/add': dynamic_block.add,
            '/dynamic_block/remove': dynamic_block.remove,
            '/dynamic_block/update': dynamic_block.update,
            '/dynamic_block/info': dynamic_block.info,

            '/product/list': product.list,
            '/product/add': product.add,
            '/product/remove': product.remove,
            '/product/update': product.update,

            '/goods/list': goods.list,
            '/goods/add': goods.add,
            '/goods/remove': goods.remove,
            '/goods/update': goods.update,
            '/goods/query': goods.query,
            '/goods/available_region_and_zone': goods.available_region_and_zone,
            '/goods/publish': goods.publish,
            '/goods/offline': goods.offline,
            '/goods/trade_check_action_available': goods.trade_check_action_available,
            '/goods/batch_update_cvm': goods.batch_update_cvm,

            '/from_generator/add': from_generator.add,
            '/from_generator/remove': from_generator.remove,
            '/from_generator/list': from_generator.list,
            '/from_generator/get_cloud_product_name': from_generator.get_cloud_product_name,

            '/blacklist/list': blacklist.list,
            '/blacklist/add': blacklist.add,
            '/blacklist/do_action': blacklist.do_action,
            '/blacklist/update': blacklist.update,

            '/tof/send_mail': api_tof.send_mail,
            '/tof/send_rtx': api_tof.send_rtx,
            '/tof/send_wx': api_tof.send_wx,
            '/tof/send_alarm': api_tof.send_alarm,
            '/tof/check_login': api_tof.check_login,
            '/tof/module_report_stat': api_tof.module_report_stat,
            '/tof/module_report_stat_list': api_tof.module_report_stat_list,
            '/tof/module_report_stat_push': api_tof.module_report_stat_push,
            '/tof/sync_module_report': api_tof.sync_module_report,

            '/activity_category/add': activity_category.add,
            '/activity_category/remove': activity_category.remove,
            '/activity_category/update': activity_category.update,
            '/activity_category/list': activity_category.list,

            '/goods_pacakge/package_add': goods_pacakge.package_add,
            '/goods_pacakge/package_remove': goods_pacakge.package_remove,
            '/goods_pacakge/package_update': goods_pacakge.package_update,
            '/goods_pacakge/package_list': goods_pacakge.package_list,
            '/goods_pacakge/package_item_list': goods_pacakge.package_item_list,
            '/goods_pacakge/package_item_add': goods_pacakge.package_item_add,
            '/goods_pacakge/package_item_remove': goods_pacakge.package_item_remove,
            '/goods_pacakge/package_combine_list': goods_pacakge.package_combine_list,
            '/goods_pacakge/package_combine_build': goods_pacakge.package_combine_build,
            '/goods_pacakge/static_package_add': goods_pacakge.static_package_add,
            '/goods_pacakge/static_package_remove': goods_pacakge.static_package_remove,
            '/goods_pacakge/static_package_update': goods_pacakge.static_package_update,
            '/goods_pacakge/static_package_list': goods_pacakge.static_package_list,
            '/goods_pacakge/static_package_detail': goods_pacakge.static_package_detail,

            '/exclusive_package/exclusive_package_add': exclusive_package.exclusive_package_add,
            '/exclusive_package/exclusive_package_remove': exclusive_package.exclusive_package_remove,
            '/exclusive_package/exclusive_package_update': exclusive_package.exclusive_package_update,
            '/exclusive_package/exclusive_package_list': exclusive_package.exclusive_package_list,
            '/exclusive_package/exclusive_package_detail': exclusive_package.exclusive_package_detail,
            '/exclusive_package/generate_exclusive_key': exclusive_package.generate_exclusive_key,
            '/exclusive_package/get_goods_list_url': exclusive_package.get_goods_list_url,

            '/exclusive_package_approval/get_approval_flow_info': exclusive_package_approval.get_approval_flow_info,
            '/exclusive_package_approval/create_approval': exclusive_package_approval.create_approval,
            '/exclusive_package_approval/approval_detail': exclusive_package_approval.approval_detail,
            '/exclusive_package_approval/approval_callback': exclusive_package_approval.approval_callback,

            '/voucher/list': voucher.list,
            '/voucher/recreate_policy': voucher.recreate_policy,
            '/voucher/get': voucher.get,
            '/voucher/remove': voucher.remove,
            '/voucher/update': voucher.update,
            '/voucher/query_received_num': voucher.query_received_num,
            '/voucher/transit_approval': voucher.transit_approval,

            '/goods_discount/price_item_build': goods_discount.price_item_build,
            '/goods_discount/price_item_list': goods_discount.price_item_list,
            '/goods_discount/get_goods_discount': goods_discount.get_goods_discount,
            '/goods_discount/set_goods_discount': goods_discount.set_goods_discount,
            '/goods_discount/activate_trade_goods_discount': goods_discount.activate_trade_goods_discount,
            '/goods_discount/copy_goods_discount': goods_discount.copy_goods_discount,
            '/goods_discount/get_config': api_goods_config.get_config,
            '/goods_discount/flush_goods_discount': goods_discount.flush_goods_discount,

            '/activity_stat/wx_interact': activity_stat.interaction_handler,
            '/activity_stat/sync': activity_stat.sync_stat,
            '/activity_stat/notice_overdue_activity': activity_stat.notice_overdue_activity,
            '/activity_stat/goods_price_export': activity_stat.goods_price_export,
            '/activity_stat/dynamic_block_subscribe_notice': activity_stat.dynamic_block_subscribe_notice,
            '/activity_stat/score_convert_scan_uin_privilege': activity_stat.score_convert_scan_uin_privilege,
            '/activity_stat/score_convert_renew_uin_score': activity_stat.score_convert_renew_uin_score,
            '/activity_stat/dapan_daily_summary': activity_stat.dapan_daily_summary,
            '/activity_stat/add_activity_to_sync': activity_stat.add_activity_to_sync,
            '/activity_stat/get_all_sync_activity': activity_stat.get_all_sync_activity,
            '/activity_stat/get_goods_consume_num': activity_stat.get_goods_consume_num,
            '/activity_stat/double_11_2019_pre_backend': activity_stat.double_11_2019_pre_backend,
            '/activity_stat/notice_user_expiring_pick_up_code': activity_stat.notice_user_expiring_pick_up_code,
            '/activity_stat/notice_activity_free_user_back_to_buy': activity_stat.notice_activity_free_user_back_to_buy,
            '/activity_stat/backend_clean_quit_staff': activity_stat.backend_clean_quit_staff,

            '/activity/anti_brush_caller': activity.anti_brush_caller,

            '/goods/approval_query': goods_approval.query,
            '/goods/approval': goods_approval.approval,
            '/goods/approval_callback': goods_approval.approval_callback,
            '/goods/goods_list': goods_approval.goods_list,
            '/goods/approver_and_leader': goods_approval.approver_and_leader,
            '/goods/simple_approval_callback': goods_approval.simple_approval_callback,

            '/activity/approval_query': activity_approval.query,
            '/activity/approval': activity_approval.approval,
            '/activity/approval_callback': activity_approval.approval_callback,
            '/activity/approver_and_leader': activity_approval.approver_and_leader,

            '/approval/list': approval.list,
            '/approval/query': approval.query,

            '/test_white_list/add': test_white_list.add,
            '/test_white_list/list': test_white_list.list,
            '/test_white_list/delete': test_white_list.remove,

            '/alert/goods_alert': alert.goods_alert,

            '/goods_config/cvm_get_instance_type': api_goods_config.cvm_get_instance_type,
            '/goods_config/cvm_get_image': api_goods_config.cvm_get_image,
            '/goods_config/cvm_get_summary_config': api_goods_config.cvm_get_summary_config,

            '/voucher_tools/query_voucher': voucher_tools.query_voucher,
            '/voucher_tools/discard_voucher':voucher_tools.discard_voucher,
            '/voucher_tools/get_op_flow': voucher_tools.get_op_flow,

            '/score_convert/list': score_convert.list,
            '/score_convert/convert_result_clear': score_convert.convert_result_clear,
            '/score_convert/convert_result_recover': score_convert.convert_result_recover,
            '/score_convert/user_list': score_convert.user_list,
            '/score_convert/user_add': score_convert.user_add,
            '/score_convert/user_del': score_convert.user_del,
            '/score_convert/goods_list': score_convert.goods_list,
            '/score_convert/goods_add': score_convert.goods_add,
            '/score_convert/goods_del': score_convert.goods_del,
            '/score_convert/goods_online': score_convert.goods_online,
            '/score_convert/goods_offline': score_convert.goods_offline,
            '/score_convert/goods_update': score_convert.goods_update,
            '/convert/convert_result': score_convert.convert_result_crontab_mail,
            '/convert/output_used_scores_and_reserved_scores': score_convert.output_used_scores_and_reserved_scores,

            '/comm_form/get_list': comm_form.get_list,
            '/comm_form/approve': comm_form.approve,
            '/comm_form/approval_reminder': comm_form.approval_reminder,

            '/template_page/detail': m_template_page.template_page_detail,
            '/template_page/list': m_template_page.template_page_list,
            '/template_page/add': m_template_page.template_page_add,
            '/template_page/update': m_template_page.template_page_update,
            '/template_page/delete': m_template_page.template_page_delete,
            '/template_page/offline': m_template_page.template_page_offline,
            '/template_page/submit_approval': m_template_page.submit_approval,
            '/template_page/publish': m_template_page.template_page_publish,
            '/template_page/reset_to_version': m_template_page.reset_to_version,
            '/template_page/approval_list': m_template_page.approval_list,
            '/template_page/approval_callback': m_template_page.approval_callback,
            '/template_page/released_list': m_template_page.template_page_release_list,
            '/template_page/save_preview': m_template_page.save_template_page_preview,

            '/comm_form/approval_download': comm_form.download_list,
        }

        for url in post_urls:
            blue.add_url_rule(url, url.replace('/', '_'), post_urls[url], methods=('OPTIONS', 'POST'))






