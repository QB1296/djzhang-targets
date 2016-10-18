import json


class ProductJsonSupport(object):
    def __init__(self):
        self.debug_folder = "/Users/djzhang/Desktop/VPS/djzhang-targets/cwotto/debug"
        super(ProductJsonSupport, self).__init__()

    def get_variation_json(self):
        data = []
        variations__json = "Apple_iPhone_SE_4/variations/535544121.json"
        json_file = "{}/{}".format(self.debug_folder, variations__json)
        with open(json_file) as data_file:
            data = json.load(data_file)

        return data[0]

    def get_product_json(self):
        data = None
        json_file = "{}/{}".format(self.debug_folder, "Apple_iPhone_SE_4/product.json")
        with open(json_file) as data_file:
            data = json.load(data_file)

        return data['variationTree']
