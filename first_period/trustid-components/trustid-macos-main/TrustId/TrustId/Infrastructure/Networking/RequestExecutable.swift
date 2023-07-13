//
//  RequestExecutable.swift
//  TrustId
//
//  Created by Adamos Adamou on 8/12/21.
//

import Foundation

protocol RequestExecutable{
    associatedtype R: Decodable
    func execute(completion: @escaping (Result<R, HttpClientError>)->Void)
}
