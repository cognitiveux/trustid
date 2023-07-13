//
//  HttpClient.swift
//  
//
//  Created by Adamos Adamou on 20/1/21.
//

import Foundation

protocol HttpClient {
    func execute<T: Decodable>(request:URLRequest, completion: @escaping (Result<T, HttpClientError>)->Void)
}
