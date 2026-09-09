// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter_test/flutter_test.dart';

import 'package:client/main.dart';

void main() {
  testWidgets('Verifica carregamento inicial do catálogo de produtos', (WidgetTester tester) async {
    // Constrói nosso app e renderiza um frame
    await tester.pumpWidget(const MyApp());

    // Verifica se o título da AppBar é exibido
    expect(find.text('Produtos (API Externa)'), findsOneWidget);
  });
}
