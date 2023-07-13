//
//  RequestBody.swift
//  
//
//  Created by Adamos Adamou on 21/1/21.
//

import Foundation

protocol RequestBody {
    associatedtype B: Encodable
    var body: B? { get }
}
