//
//  MockAlertService.swift
//  TrustId
//
//  Created by Adamos Adamou on 23/1/22.
//

import Foundation
import SwiftUI

struct MockAlertService{
    public static let alerts:[AlertListView.Alert] = [
        .init(text: "Some alert 1", statusColor: .green),
        .init(text: "Some alert 2. Alert with longer text hopefully 2 lines size of description", statusColor: .green),
        .init(text: "Some alert 3", statusColor: .red)
    ]
}
