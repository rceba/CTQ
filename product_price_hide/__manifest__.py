# Copyright 2020 Morwi Encoders Consulting SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Product Price Hide',
    'version': "17.0.1.0.0",
    'category': 'Sales/Sales',
    'author': 'Morwi Encoders',
    'summary': 'Hide price from product form',
    'license': 'LGPL-3',
    'depends': [ 'sale_management' ],
    'description': "Hide the sales price from the product form and display the pricelist entries under the sales tab",
    'data': [ 'security/security.xml','views/product_views.xml' ],
}
