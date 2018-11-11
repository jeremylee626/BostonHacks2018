//
//  ViewController.swift
//  BostonHacks2018
//
//  Created by Jeremy Lee on 11/10/18.
//  Copyright © 2018 Jeremy Lee. All rights reserved.
//

import UIKit
import CoreLocation
import MessageUI

class TipViewController: UIViewController {
    
    // MARK: - Variables
    var locationManager = CLLocationManager()
    var longitude: CLLocationDegrees?
    var latitude: CLLocationDegrees?
    var sentDateTime: String?
    @IBOutlet weak var messageView: UIView!
    @IBOutlet weak var titleView: UIView!
    
    
    // MARK: - Outlets
    @IBOutlet weak var tipTextView: UITextView!
    @IBOutlet weak var submitButton: UIButton!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Create tool bar for text view
        createToolbar(chosenTextView: tipTextView)
        
        messageView.layer.cornerRadius = 10.0
        messageView.layer.masksToBounds = true
        
        tipTextView.layer.cornerRadius = 10.0
        
    }
    
    @IBAction func submitButton(_ sender: UIButton) {
        // Create date formatter
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "MMMM dd, yyyy 'at' h:mm:ss a"
        
        // Format current date
        sentDateTime = dateFormatter.string(from: Date())
        
        // Send message
        displayMessageInterface()
    }
    
    @IBAction func cancelButtonPressed(_ sender: UIButton) {
    }
    
    
    func createToolbar(chosenTextView: UITextView) {
        let toolbar = UIToolbar()
        toolbar.sizeToFit()
        toolbar.backgroundColor = #colorLiteral(red: 0.6000000238, green: 0.6000000238, blue: 0.6000000238, alpha: 1)
        
        let doneButton = UIBarButtonItem(title: "Done", style: .done, target: self, action: #selector(TipViewController.doneButtonPressed))
        let flexibleSpace = UIBarButtonItem(barButtonSystemItem: .flexibleSpace, target: nil, action: nil)
        
        toolbar.setItems([flexibleSpace, doneButton, flexibleSpace], animated: false)
        chosenTextView.inputAccessoryView = toolbar
    }
    
    @objc func doneButtonPressed() {
        view.endEditing(true)
    }
    
}

extension TipViewController: MFMessageComposeViewControllerDelegate {
    func messageComposeViewController(_ controller: MFMessageComposeViewController, didFinishWith result: MessageComposeResult) {
        controller.dismiss(animated: true, completion: nil)
    }
    
    func displayMessageInterface() {
        let composeVC = MFMessageComposeViewController()
        composeVC.messageComposeDelegate = self
        
        // Phone number to text
        composeVC.recipients = ["7812414653"]
        
        // Message to send
        let message = tipTextView.text ?? "No Message..."
        let gpsLocation = "(Long: \(longitude ?? 0.0), Lat: \(latitude ?? 0.0))\n"
        composeVC.body = message + "\n" + gpsLocation + "Sent: " + (sentDateTime ?? "Error setting Date...")
        
        
        if MFMessageComposeViewController.canSendText() {
            self.present(composeVC, animated: true, completion: nil)
        } else {
            print("Can't send messages")
        }
        
    }
    
    
}
