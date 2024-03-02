import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../settings/settings_view.dart';
import 'item.dart';
import 'min_list_view.dart';
import 'package:firebase_database/firebase_database.dart';

class DateListView extends StatefulWidget {
  const DateListView({super.key});
  static const routeName = '/datelistview';
  
  @override
  State<DateListView> createState() => _DateListViewState();
}
  
class _DateListViewState extends State<DateListView> {
  final rtdatabase _database = rtdatabase(); // Create an instance of your rtdatabase class

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Unrecognised Faces'),
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
            // Assuming snapshot.data is the data you retrieved from the database
            DataSnapshot itemSnapshot = snapshot.data as DataSnapshot;
            Map? items = itemSnapshot.value as Map?;
            log("as");
            return ListView.builder(
              restorationId: 'sampleItemListView',
              itemCount: items?.length,
              itemBuilder: (BuildContext context, int index) {
                // Assuming each item in the list is a string
                String itemName = '';
                String formattedDate = '';
                if (items != null) {
                  // Retrieve keys as a list and get the key at the specified index
                  List keys = items.keys.toList();
                  
                  if (index < keys.length) {
                    itemName = keys[index];
                    //convert unix to dd-mmm-yyyy
                    DateTime dateTime = DateTime.fromMillisecondsSinceEpoch(int.parse(itemName) * 1000);
                    formattedDate = DateFormat('dd-MMM-yyyy').format(dateTime).toString();
                  }
                }
                return ListTile(
                  title: Text(formattedDate),
                  onTap: () {
                    String variableToPass = itemName;
                    Navigator.restorablePushNamed(
                      context,
                      MinListView.routeName,
                      arguments: variableToPass,
                    );
                  },
                );
              },
            );
          }
        },
        ),
        floatingActionButton: FloatingActionButton(onPressed: () {  },
        //onPressed: () => setState(() => propList.add('text')),
        //child: Icon(Icons.add),
      ),);
    }
  }