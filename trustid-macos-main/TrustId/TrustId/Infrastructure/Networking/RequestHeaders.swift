//
//  RequestHeaders.swift
//  TrustId
//
//  Created by Adamos Adamou on 9/12/21.
//

import Foundation

protocol RequestHeaders{
    var headers: [HttpHeader] { get }
}
