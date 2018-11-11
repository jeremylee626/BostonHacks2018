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
    var newPin = MKPointAnnotation()
    
    // MARK: Outlets
    @IBOutlet weak var mapView: MKMapView!
    
    // MARK: Actions
    @IBAction func sendTipButtonPressed(_ sender: UIBarButtonItem) {
        performSegue(withIdentifier: "goToTipVC", sender: self)
    }
    
    // MARK: Functions
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Set location manager delegate
        locationManager.delegate = self
        
        // Setting location accuracy
        locationManager.desiredAccuracy = kCLLocationAccuracyHundredMeters
        
        // Prompt user for authorization to access his/her location
        locationManager.requestWhenInUseAuthorization()
        
        // Prompts locationManager to look for GPS location
        locationManager.startUpdatingLocation()
        
//        // Add a gesture recognizer
//        var gestureRecognizer = UILongPressGestureRecognizer(target: self, action: <#T##Selector?#>)
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
        
        // Longitude and latitude
        latitude = location.coordinate.latitude
        longitude = location.coordinate.longitude
        
        // Set current location
        let currentLocation = CLLocationCoordinate2D(latitude: latitude ?? 0.0 , longitude: longitude ?? 0.0)
        print(latitude ?? 0.0)
        print(longitude ?? 0.0)
        
        centerMapLocation(location: currentLocation)
        
        newPin.coordinate = location.coordinate
        mapView.addAnnotation(newPin)
    }
    
}

