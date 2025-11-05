class Holding {
  final String assetSymbol;
  final String assetName;
  final String assetType;
  final double quantity;
  final double purchasePrice;
  final double currentPrice;
  final DateTime purchaseDate;
  final double currentValue;
  final double totalCost;
  final double gainLoss;
  final double gainLossPercentage;

  Holding({
    required this.assetSymbol,
    required this.assetName,
    required this.assetType,
    required this.quantity,
    required this.purchasePrice,
    required this.currentPrice,
    required this.purchaseDate,
    required this.currentValue,
    required this.totalCost,
    required this.gainLoss,
    required this.gainLossPercentage,
  });

  factory Holding.fromJson(Map<String, dynamic> json) {
    return Holding(
      assetSymbol: json['asset_symbol'],
      assetName: json['asset_name'],
      assetType: json['asset_type'],
      quantity: double.parse(json['quantity'].toString()),
      purchasePrice: double.parse(json['purchase_price'].toString()),
      currentPrice: double.parse(json['current_price'].toString()),
      purchaseDate: DateTime.parse(json['purchase_date']),
      currentValue: double.parse(json['current_value'].toString()),
      totalCost: double.parse(json['total_cost'].toString()),
      gainLoss: double.parse(json['gain_loss'].toString()),
      gainLossPercentage: double.parse(json['gain_loss_percentage'].toString()),
    );
  }
}