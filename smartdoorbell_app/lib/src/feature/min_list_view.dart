import 'dart:math';

import 'package:flutter/material.dart';
import '../settings/settings_view.dart';
import 'item.dart';
import 'package:firebase_database/firebase_database.dart';
import 'package:intl/intl.dart';

class MinListView extends StatefulWidget {
  final String dateHour;
  //  const MinListView({Key? key, required this.dateHour}) : super(key: key);

  const MinListView({super.key, required this.dateHour});
  static const routeName = '/minlistview';
  
  @override
  State<MinListView> createState() => _MinListViewState();
}
  
class _MinListViewState extends State<MinListView> {
  final rtdatabase _database = rtdatabase(); // Create an instance of your rtdatabase class
  @override
  Widget build(BuildContext context) {
    String dateHour = ModalRoute.of(context)!.settings.arguments as String;
    DateTime dateTime = DateTime.fromMillisecondsSinceEpoch(int.parse(dateHour) * 1000);
    String formattedDate = DateFormat('dd-MMM-yyyy').format(dateTime).toString();

    return Scaffold(
      appBar: AppBar(
        title: Text(formattedDate),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              Navigator.restorablePushNamed(context, SettingsView.routeName);
            },
          ),
        ],
      ),
      body: FutureBuilder(
        future: _database.get(), // Call the get() function from rtdatabase class
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const CircularProgressIndicator();
          } else if (snapshot.hasError) {
            return Text('Error: ${snapshot.error}');
          } else {
            DataSnapshot itemSnapshot = snapshot.data as DataSnapshot;
            Map? parentItems = itemSnapshot.value as Map?;
            Map? items = parentItems?[dateHour] as Map?;
            log(0);
            return ListView.builder(
              restorationId: 'sampleItemListView',
              itemCount: items?.length,
              itemBuilder: (BuildContext context, int index) {
                if (items == null) {
                  return const Center(child: CircularProgressIndicator());
                }
                
                String itemName = '';
                String formattedTime = '';
                List keys = items.keys.toList();
                keys.sort((a, b) => b.compareTo(a));
                String imageUrl = '';

                if (index < keys.length) {
                  itemName = keys[index];
                  
                  DateTime dateTime = DateTime.fromMillisecondsSinceEpoch(int.parse(itemName) * 1000);
                  formattedTime = "${DateFormat('HH:mm').format(dateTime)} Hrs";

                  items[itemName].forEach((key, value) {
                    if (key == 'url') {
                      imageUrl = value;
                    }
                  });
                }
                return Column(
                  children: [
                    SizedBox(
                        width: 375,
                        height: 375,
                        child: Image.network(imageUrl),
                    ),
                    SizedBox(
                      width: 375,
                      child: Center(
                        child: Text(formattedTime),
                      ),
                    ),
                  ],
                );
              },
            );
          }
        },
      ),
    );
    }
  }