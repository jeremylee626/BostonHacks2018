//
//  MapViewController.swift
//  BostonHacks2018
//
//  Created by Jeremy Lee on 11/11/18.
//  Copyright © 2018 Jeremy Lee. All rights reserved.
//

import UIKit
import MapKit
import CoreLocation

class MapViewController: UIViewController {
    
    // MARK: Properties
    var locationManager = CLLocationManager()
    var latitude: CLLocationDegrees?
    var longitude: CLLocationDegrees?
    var pinsArray = [MKPointAnnotation]()
    var currentPin = MKPointAnnotation()
    var message: String?
    @IBOutlet weak var sendMessageButton: UIButton!
    
    
    // MARK: Outlets
    @IBOutlet weak var mapView: MKMapView!
    
    // MARK: Actions
    @IBAction func sendFromCurrentLocationPressed(_ sender: UIButton) {
        performSegue(withIdentifier: "goToTipVC", sender: self)
    }
    
    
    // MARK: Functions
    
    override func viewDidLoad() {
        super.viewDidLoad()
        navigationItem.title = "Hotline Bling"
        navigationController?.navigationBar.prefersLargeTitles = true
        
        // Set location manager delegate
        locationManager.delegate = self
        
        // Setting location accuracy
        locationManager.desiredAccuracy = kCLLocationAccuracyHundredMeters
        
        // Prompt user for authorization to access his/her location
        locationManager.requestWhenInUseAuthorization()
        
        // Prompts locationManager to look for GPS location
        locationManager.startUpdatingLocation()
        
        // Add a gesture recognizer
        let gestureRecognizer = UILongPressGestureRecognizer(target: self, action: #selector(addPin(gestureRecognizer:)))
        gestureRecognizer.minimumPressDuration = 0.5
        mapView.addGestureRecognizer(gestureRecognizer)
        
        // Format send message button
        sendMessageButton.layer.cornerRadius = 10.0
        
    }
    
    @objc func addPin(gestureRecognizer: UIGestureRecognizer) {
        if gestureRecognizer.state == .began {
            print("touch")
            let touchPoint = gestureRecognizer.location(in: mapView)
            let coordinates = mapView.convert(touchPoint, toCoordinateFrom: mapView)
            let newPin = MKPointAnnotation()
            newPin.coordinate = coordinates
            
            
//            let pinToAdd = MKPointAnnotation()
//            pinToAdd.coordinate = coordinates
            pinsArray.append(newPin)
            mapView.addAnnotation(newPin)
            
            longitude = newPin.coordinate.longitude
            latitude = newPin.coordinate.latitude
            
            performSegue(withIdentifier: "goToTipVC", sender: self)
        }
        
    }
    
    func centerMapLocation(location: CLLocationCoordinate2D) {
        let regionRadius: CLLocationDistance = 1000
        let zoomRegion = MKCoordinateRegion(center: location, latitudinalMeters: regionRadius, longitudinalMeters: regionRadius)
        mapView.setRegion(zoomRegion, animated: true)
        
    }
    
    // MARK: Navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        let destinatiionVC = segue.destination as! TipViewController
        destinatiionVC.latitude = latitude
        destinatiionVC.longitude = longitude
    }
    
    @IBAction func unwindToMapVC(_ segue: UIStoryboardSegue) {
        if pinsArray.count > 0 {
            if let activityMessage = message {
                pinsArray.last?.subtitle = activityMessage
            }
            print(mapView.annotations)
            for pin in pinsArray {
                if pin.subtitle == "Empty" {
                    mapView.removeAnnotation(pin)
                }
            }
        }
        
    }
    
}

extension MapViewController: CLLocationManagerDelegate {
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        
        // Store mose accurate GPS location
        let location = locations[locations.count - 1]
        
        // Make sure location is valid
        if location.horizontalAccuracy > 0 {
            // Stop updating GPS location
            locationManager.stopUpdatingLocation()
            locationManager.delegate = nil
        }
        
        // Longitude and latitude of user's current location
        latitude = location.coordinate.latitude
        longitude = location.coordinate.longitude
        
        // Set current location
        let currentLocation = CLLocationCoordinate2D(latitude: latitude ?? 0.0 , longitude: longitude ?? 0.0)
        print(latitude ?? 0.0)
        print(longitude ?? 0.0)
        
        // Center map on current location
        centerMapLocation(location: currentLocation)
        
        // Create pin at user's current location
        currentPin.coordinate = location.coordinate
        currentPin.title = "You are here"
        mapView.addAnnotation(currentPin)

    }
    
}

