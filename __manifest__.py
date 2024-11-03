{
  'name': 'qwe Prime Delivery API',
  'version': '1.0',
  'category': 'Custom',
  'author': 'Yousif Basil',
  'summary': 'API for Primte Company to Update Order Status',
  'depends': ['sale', 'stock','website'],  
  'data': [
      
      'security/ir.model.access.csv',
      'views/views.xml',
      'views/state_view.xml', 
      'views/district_view.xml', 
      'views/res_partner.xml', 
      'views/account_move.xml',
      'views/sale_order_views.xml',
      'views/delivery_tracking_template.xml',
  ],
  'installable': True,
  'application': False,
# you need to install html2text run this please
  # pip3 install html2text
}
