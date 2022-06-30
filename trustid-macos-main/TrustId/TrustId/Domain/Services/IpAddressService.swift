//
//  IpAddressService.swift
//  TrustId
//
//  Created by Adamos Adamou on 14/12/21.
//

import Foundation
import SwiftPublicIP

struct IpAddressService{
    public func execute(completionHandler: @escaping (String)->Void){
        SwiftPublicIP.getPublicIP(url: PublicIPAPIURLs.ipv4.icanhazip.rawValue) { (string, error) in
            if let error = error {
                print(error.localizedDescription)
                completionHandler("-")
            } else if let string = string {
                completionHandler(string)
            }
        }
    }
}
