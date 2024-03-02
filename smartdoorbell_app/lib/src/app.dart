import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';
import 'package:flutter_gen/gen_l10n/app_localizations.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

import 'feature/item_details_view.dart';
import 'feature/date_list_view.dart';
import 'feature/min_list_view.dart';
import 'settings/settings_controller.dart';
import 'settings/settings_view.dart';
import 'authentication/login.dart';
import 'authentication/create_account.dart';

/// The Widget that configures your application.
class MyApp extends StatelessWidget {
  const MyApp({
    super.key,
    required this.settingsController,
  });

  final SettingsController settingsController;
  
  @override
  void initState() {
    // Remove the line below since MyApp does not have a superclass with an initState method.
    // super.initState();
    // Handle incoming messages
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      // Handle the message
      print("Received message: ${message.notification?.title}");
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: settingsController,
      builder: (BuildContext context, Widget? child) {
        return MaterialApp(
          restorationScopeId: 'app',
          localizationsDelegates: const [
            AppLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
          ],
          supportedLocales: const [
            Locale('en', ''), // English, no country code
          ],
          onGenerateTitle: (BuildContext context) =>
              AppLocalizations.of(context)!.appTitle,
          theme: ThemeData(),
          darkTheme: ThemeData.dark(),
          themeMode: settingsController.themeMode,
          onGenerateRoute: (RouteSettings routeSettings) {
            return MaterialPageRoute<void>(
              settings: routeSettings,
              builder: (BuildContext context) {
                switch (routeSettings.name) {
                  case LoginView.routeName:
                    return LoginView();
                  case CreateAccountView.routeName:
                    return CreateAccountView();
                  case SettingsView.routeName:
                    return SettingsView(controller: settingsController);
                  case ItemDetailsView.routeName:
                    return const ItemDetailsView();
                  case DateListView.routeName:
                    return const DateListView();
                  case MinListView.routeName:
                    return const MinListView(dateHour: '',);
                  default:
                    return LoginView();
                }
              },
            );
          },
        );
      },
    );
  }
}
