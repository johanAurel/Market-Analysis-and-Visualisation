{ 'name': 'USD_CNH', 'type': 'CURRENCY', 'displayName': 'USD/CNH',
  'pipLocation': -4, 'displayPrecision': 5,
  'tradeUnitsPrecision': 0, 'minimumTradeSize': '1',
  'maximumTrailingStopDistance': '1.00000', 
  'minimumTrailingStopDistance': '0.00050', 
  'maximumPositionSize': '0', 
  'maximumOrderUnits': '100000000', 
  'marginRate': '0.05',
  'guaranteedStopLossOrderMode': 'DISABLED', 
  'tags': [{'type': 'ASSET_CLASS', 'name': 'CURRENCY'}, 
           {'type': 'BRAIN_ASSET_CLASS', 'name': 'FX'}], 
  'financing': 
    {
        'longRate': '0.0244', 'shortRate': '-0.051', 
        
        'financingDaysOfWeek': [
            {'dayOfWeek': 'MONDAY', 'daysCharged': 1},
            {'dayOfWeek': 'TUESDAY', 'daysCharged': 1}, {'dayOfWeek': 'WEDNESDAY', 'daysCharged': 1}, 
            {'dayOfWeek': 'THURSDAY', 'daysCharged': 1}, {'dayOfWeek': 'FRIDAY', 'daysCharged': 1},
            {'dayOfWeek': 'SATURDAY', 'daysCharged': 0}, {'dayOfWeek': 'SUNDAY', 'daysCharged': 0}
        ]
    }
}
