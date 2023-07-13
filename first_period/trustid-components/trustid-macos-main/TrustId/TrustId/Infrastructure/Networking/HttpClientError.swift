//
//  HttpClientError.swift
//  
//
//  Created by Adamos Adamou on 20/1/21.
//

import Foundation

enum HttpClientError:Error{
    case failed(Error)
    case noData
    case apiErrorResponse(Int, HttpClientErrorModel)
}
