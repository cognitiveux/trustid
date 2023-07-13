//
//  PageRoute.swift
//  TrustId
//
//  Created by Adamos Adamou on 29/11/21.
//

import Foundation

enum PageRoute{
    case Dashboard
    case Examination
    case Exam(examId:String)
    // case Settings
    case Profile
}

extension PageRoute:Equatable{ }
