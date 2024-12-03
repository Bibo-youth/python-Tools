from collections import deque
from difflib import SequenceMatcher

class KeyValuePath:
    def __init__(self, key, value, path):
        self.key = key
        self.value = value
        self.path = path
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def findAndAssign(source, target):
    # def getSorKkey(x, reference_key):
    #     """
    #     x: 要比较的对象。
    #     reference_key: 参考键，用于计算当前键与之的相似度
    #     元祖顺序代表比较的优先级
    #     """
    #     path_length = len(x.path)
    #     key_similarity = similar(x.key, reference_key)
    #     path = x.path
    #     return (path_length, key_similarity, path)

    def traverse(key, value, current_path):
        matches = []
        traverseTarget(target, deque(), key, value, current_path, matches)
        if matches:
            # 如果有多个匹配，保存路径深度最大且键名相似度最高的
            best_match = max(matches, key=lambda x: (len(x.path), similar(x.key, key), x.path))
            # print(f"Best match for key '{key}' with path {best_match.path} and similarity {similar(best_match.key, key):.2f}")
            yield key, best_match.value
        else:
            # 如果没有匹配，保持原来的值
            yield key, value

    def traverseSource(src, path=deque()):
        if isinstance(src, dict):
            for key, value in src.items():
                path.append(key)
                current_path = tuple(path)
                yield from traverse(key, value, current_path)
                path.pop()
        elif isinstance(src, list):
            for index, item in enumerate(src):
                path.append(f'[{index}]')
                current_path = tuple(path)
                yield from traverse(f'[{index}]', item, current_path)
                path.pop()

    def traverseTarget(trg, path, src_key, src_value, src_path, matches):
        if isinstance(trg, dict):
            for key, value in trg.items():
                new_path = path + deque([key])
                if key == src_key:
                    matches.append(KeyValuePath(key, value, new_path))
                traverseTarget(value, new_path, src_key, src_value, src_path, matches)
        elif isinstance(trg, list):
            for index, item in enumerate(trg):
                new_path = path + deque([f'[{index}]'])
                traverseTarget(item, new_path, src_key, src_value, src_path, matches)
                # 构建更新后的字典

    updated_dict = {}
    for key, value in traverseSource(source):
        if isinstance(value, dict) or isinstance(value, list):
            # 如果值是字典或列表，递归处理
            updated_dict[key] = findAndAssign(value, target) if isinstance(value, dict) else [
                findAndAssign(item, target) for item in value]
        else:
            updated_dict[key] = value
    return updated_dict

if __name__ == '__main__':
    target1 = {
    "OrderRespMap": {
        "4611686102279981575": {
            "ShopOrder": {
                "ShopOrderID": "4611686102279981575",
                "BuyOrderID": "4611686102296758791",
                "UserID": 7395136801214039046,
                "MerchantID": 100000002954497,
                "BizLine": 1,
                "OrderStatus": 100,
                "Region": "ID",
                "AmountDetail": {
                    "SaleAmount": "1000000",
                    "PayAmount": "1000000",
                    "DiscountAmount": "1000000",
                    "Currency": "IDR"
                },
                "CreateTime": 1721833462,
                "UpdateTime": 1721833462,
                "SkuOrderCount": 1,
                "ItemOrderCount": 1,
                "ReviewStatus": 0,
                "Version": 0,
                "ExpireTime": 1721840662
            },
            "SkuOrderMap": {
                "6424321": {
                    "SkuID": 6424321,
                    "SkuNum": 1,
                    "SkuName": "hzf close loop no4",
                    "SkuI18nName": "{\"default_text\":\"hzf close loop no4\",\"translations\":{\"id\":\"hzf close loop no4\"}}",
                    "SkuVersion": 1,
                    "AmountDetail": {
                        "SaleAmount": "1000000",
                        "PayAmount": "1000000",
                        "DiscountAmount": "0",
                        "Currency": "IDR",
                        "CrossedAmount": "2000000"
                    },
                    "ProductID": 6423553,
                    "ProductName": "hzf close loop no4",
                    "ProductI18nName": "{\"default_text\":\"勿动 - hzf close loop no4\",\"translations\":{\"id\":\"hzf close loop no4\"}}",
                    "ProductType": 2,
                    "ProductImageUri": "dab834a4f5d4f169664bd24be999b665",
                    "CategoryID": 24020101,
                    "BuyLimit": 10,
                    "LimitBuyRule": "{\"enable_limit\":true,\"rule_list\":[{\"subject_type\":1,\"range_type\":3,\"limit_num\":1000,\"unit\":\"\",\"dimension_type\":null},{\"subject_type\":1,\"range_type\":2,\"limit_num\":10,\"unit\":\"\",\"dimension_type\":null}]}",
                    "UseDate": "{\"use_date_type\":2,\"day_duration\":30}",
                    "RefundPolicy": "null",
                    "SkuAttrList": "[{\"assembly_type\":3,\"attr_key\":\"origin_amount\",\"i18n_ttr_key_name\":{\"default_text\":\"Total price of the product \"},\"attr_key_name\":null,\"attr_value\":\"1.000.000\",\"is_multi\":false,\"attr_type\":100},{\"assembly_type\":3,\"attr_key\":\"actual_amount\",\"i18n_ttr_key_name\":{\"default_text\":\"Customers actually need to pay\"},\"attr_key_name\":null,\"attr_value\":\"2.000.000\",\"is_multi\":false,\"attr_type\":100},{\"assembly_type\":3,\"attr_key\":\"local_currency\",\"i18n_ttr_key_name\":{\"default_text\":\"local currency\"},\"attr_key_name\":null,\"attr_value\":\"IDR\",\"is_multi\":false,\"attr_type\":100},{\"assembly_type\":101,\"attr_key\":\"stock_info\",\"i18n_ttr_key_name\":{\"default_text\":\"Stock quantity\"},\"attr_key_name\":null,\"attr_value\":\"{\\\"stock_num\\\":1000,\\\"stock_qty_limit_type\\\":1}\",\"is_multi\":false,\"attr_type\":100},{\"assembly_type\":102,\"attr_key\":\"limit_buy_rule\",\"i18n_ttr_key_name\":{\"default_text\":\"Purchase restrictions\"},\"attr_key_name\":null,\"attr_value\":\"{\\\"enable_limit\\\":true,\\\"rule_list\\\":[{\\\"subject_type\\\":1,\\\"range_type\\\":3,\\\"limit_num\\\":1000},{\\\"subject_type\\\":1,\\\"range_type\\\":2,\\\"limit_num\\\":10}]}\",\"is_multi\":false,\"attr_type\":301}]",
                    "ProductAttrList": "[{\"assembly_type\":1,\"attr_key\":\"rec_person_num\",\"i18n_ttr_key_name\":{\"default_text\":\"Recommended number of people\"},\"attr_key_name\":null,\"attr_value\":\"5\",\"is_multi\":false,\"attr_type\":100},{\"assembly_type\":1,\"attr_key\":\"rec_person_num_max\",\"i18n_ttr_key_name\":{\"default_text\":\"Max number of people\"},\"attr_key_name\":null,\"attr_value\":\"20\",\"is_multi\":false,\"attr_type\":100},{\"assembly_type\":1,\"attr_key\":\"shop_id\",\"i18n_ttr_key_name\":{\"default_text\":\"Max number of people\"},\"attr_key_name\":null,\"attr_value\":\"[222]\",\"is_multi\":true,\"attr_type\":100},{\"assembly_type\":1,\"attr_key\":\"product_name\",\"i18n_ttr_key_name\":{\"default_text\":\"product name\"},\"attr_key_name\":null,\"attr_value\":\"{\\\"DefaultText\\\":\\\"product name\\\"}\",\"is_multi\":false,\"attr_type\":100},{\"assembly_type\":6,\"attr_key\":\"image_list\",\"i18n_ttr_key_name\":{\"default_text\":\"product cover image\"},\"attr_key_name\":null,\"attr_value\":\"[{\\\"uri\\\":\\\"dab834a4f5d4f169664bd24be999b665\\\"}]\",\"is_multi\":true,\"attr_type\":100},{\"assembly_type\":101,\"attr_key\":\"stock_info\",\"i18n_ttr_key_name\":{\"default_text\":\"Stock quantity\"},\"attr_key_name\":null,\"attr_value\":\"{\\\"stock_num\\\":1000,\\\"stock_qty_limit_type\\\":1}\",\"is_multi\":false,\"attr_type\":100},{\"assembly_type\":1,\"attr_key\":\"sold_start_time\",\"i18n_ttr_key_name\":{\"default_text\":\"Product sales date\"},\"attr_key_name\":null,\"attr_value\":\"1720666722\",\"is_multi\":false,\"attr_type\":100},{\"assembly_type\":1,\"attr_key\":\"sold_end_time\",\"i18n_ttr_key_name\":{\"default_text\":\"Product sales date\"},\"attr_key_name\":null,\"attr_value\":\"1752202732\",\"is_multi\":false,\"attr_type\":100},{\"assembly_type\":1,\"attr_key\":\"sold_time_type\",\"i18n_ttr_key_name\":{\"default_text\":\"Product sales date\"},\"attr_key_name\":null,\"attr_value\":\"1\",\"is_multi\":false,\"attr_type\":100},{\"assembly_type\":103,\"attr_key\":\"use_date\",\"i18n_ttr_key_name\":{\"default_text\":\"Available Dates\"},\"attr_key_name\":null,\"attr_value\":\"{\\\"use_date_type\\\":2,\\\"day_duration\\\":30}\",\"is_multi\":false,\"attr_type\":303},{\"assembly_type\":104,\"attr_key\":\"cannot_use_date\",\"i18n_ttr_key_name\":{\"default_text\":\"Unavailable Dates\"},\"attr_key_name\":null,\"attr_value\":\"{\\\"enable\\\":true,\\\"days_of_week\\\":[1],\\\"date_list\\\":[\\\"2024-08-30\\\"]}\",\"is_multi\":false,\"attr_type\":303},{\"assembly_type\":105,\"attr_key\":\"use_time\",\"i18n_ttr_key_name\":{\"default_text\":\"Daily available time\"},\"attr_key_name\":null,\"attr_value\":\"{\\\"use_time_type\\\":2,\\\"time_period_list\\\":[{\\\"use_start_time\\\":\\\"20:00\\\",\\\"use_end_time\\\":\\\"02:00\\\",\\\"end_time_is_next_day\\\":true}]}\",\"is_multi\":false,\"attr_type\":303},{\"assembly_type\":107,\"attr_key\":\"appointment\",\"i18n_ttr_key_name\":{\"default_text\":\"Reservation Rules\"},\"attr_key_name\":null,\"attr_value\":\"{\\\"need_appointment\\\":true,\\\"ahead_time_type\\\":1,\\\"ahead_num\\\":20}\",\"is_multi\":false,\"attr_type\":301},{\"assembly_type\":108,\"attr_key\":\"consumption_convention\",\"i18n_ttr_key_name\":{\"default_text\":\"Dine-in and take-out arrangements\"},\"attr_key_name\":null,\"attr_value\":\"{\\\"consumption_methods\\\":[1,2]}\",\"is_multi\":false,\"attr_type\":200},{\"assembly_type\":109,\"attr_key\":\"description_rich_text\",\"i18n_ttr_key_name\":{\"default_text\":\"Other information\"},\"attr_key_name\":null,\"attr_value\":\"{\\\"content\\\":\\\"{\\\\\\\"default_text\\\\\\\":\\\\\\\"Other information\\\\\\\"}\\\"}\",\"is_multi\":false,\"attr_type\":200}]"
                }
            },
            "ItemOrderMap": {
                "4611686105836751367": {
                    "ItemOrderID": "4611686105836751367",
                    "ShopOrderID": "4611686102279981575",
                    "UserID": 7395136801214039046,
                    "MerchantID": 100000002954497,
                    "OrderStatus": 100,
                    "TradeType": 11,
                    "SkuID": 6424321,
                    "SkuNum": 1,
                    "ProductID": 6423553,
                    "ProductType": 2,
                    "AmountDetail": {
                        "SaleAmount": "1000000",
                        "PayAmount": "1000000",
                        "DiscountAmount": "0",
                        "Currency": "IDR"
                    },
                    "CreateTime": 1721833462,
                    "UpdateTime": 1721833462,
                    "Version": 1
                }
            }
        }
    },
    "BaseResp": {
        "StatusMessage": "",
        "StatusCode": 0
    }
}
    source1 = {
    "UserID": 0,
    "BuyOrderID": "",
    "PayAmount": "",
    "Currency": "",
    "Region": "",
    "EffectiveTime": 0,
    "CreateTime": 0,
    "IsTest": False,
    "ChannelPayInfoStr": "",
    "ShopOrderList": [
        {
            "BuyOrderID": "",
            "ShopOrderID": "",
            "BizMerchantID": "",
            "AmountDetail": {
                "SaleAmount": "",
                "PayAmount": "",
                "DiscountAmount": "",
                "Currency": "",
                "TaxAmount": "",
                "CrossedAmount": ""
            },
            "CreateTime": 0,
            "DiscountDetailList": [
                {
                    "DiscountID": "",
                    "DiscountType": 0,
                    "SkuID": 0,
                    "DiscountAmount": 0,
                    "MerchantDiscountAmount": 0,
                    "PlatformDiscountAmount": 0,
                    "Currency": "",
                    "DiscountSource": 0,
                    "Extra": "",
                    "ActivityID": "",
                    "Num": 0,
                    "FunderList": [
                        {
                            "Funder": 1,
                            "FundedAmount": 0,
                            "FunderAccountID": "",                            "FunderDetails": [
                                {
                                    "Type": 1,
                                    "ParamMap": {
                                        "": ""
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ],
    "ItemOrderList": [
        {
            "BuyOrderID": "",
            "ShopOrderID": "",
            "ItemOrderID": "",
            "BizMerchantID": "",
            "AmountDetail": {
                "SaleAmount": "",
                "PayAmount": "",
                "DiscountAmount": "",
                "Currency": "",
                "TaxAmount": "",
                "CrossedAmount": ""
            },
            "FeeType": 0,
            "SkuID": "",
            "ItemNum": 0,
            "SkuName": "",
            "CreateTime": 0
        }
    ],
    "SkuDetailList": [
        {
            "SkuID": "",
            "SkuName": "",
            "AmountDetail": {
                "SaleAmount": "",
                "PayAmount": "",
                "DiscountAmount": "",
                "Currency": "",
                "TaxAmount": "",
                "CrossedAmount": ""
            },
            "BizMerchantID": "",
            "Quantity": 0,
            "Category": ""
        }
    ],
    "AppContext": {
        "PriorityRegion": "",
        "CarrierRegion": "",
        "AppRegion": "",
        "SysRegion": "",
        "StoreRegion": "",
        "CurrentRegion": "",
        "AppLanguage": "",
        "SysLanguage": "",
        "TimezoneName": "",
        "Locale": "",
        "Did": 0,
        "Aid": 0,
        "Iid": 0,
        "VersionName": "",
        "UserAgent": "",
        "AppName": "",
        "AppVersion": "",
        "Channel": "",
        "OsVersion": "",
        "VersionCode": "",
        "DevicePlatform": "",
        "Forwarded": "",
        "DeviceType": "",
        "DeviceBrand": "",
        "Ip": "",
        "SessionAid": 0,
        "SessionDid": 0,
        "SessionLoginType": "",
        "CheckSignRes": "",
        "CheckSignErr": "",
        "CheckSignResExtra": "",
        "EagleyeEnv": 0
    },
    "Base": {
        "LogID": "",
        "Caller": "",
        "Addr": "",
        "Client": "",
        "TrafficEnv": {
            "Open": False,
            "Env": ""
        },
        "Extra": {
            "": ""
        }
    }
}
    updated_dict2 = findAndAssign(source1, target1)
    print(updated_dict2)
    # print(source)
