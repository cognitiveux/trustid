//
//  EndpointRoute.swift
//  
//
//  Created by Adamos Adamou on 21/1/21.
//

import Foundation

protocol EndpointRoute{
    var path: URL { get }
    var method: HttpMethod { get }
}
