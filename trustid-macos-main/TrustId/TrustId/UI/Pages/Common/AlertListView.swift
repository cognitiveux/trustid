//
//  AlertListView.swift
//  TrustId
//
//  Created by Adamos Adamou on 19/1/22.
//

import SwiftUI

extension AlertListView{
    struct Alert:Identifiable{
        let id = UUID()
        let text:String
        let statusColor:Color
    }
}

struct AlertListView: View {
    
    public let alerts:[Alert]
    
    var body: some View {
        List(alerts){ alert in
            alertView(alert)
                .padding(8)
        }
    }
    
    private func alertView(_ alert:Alert) -> some View{
        HStack(spacing: 8){
            Circle()
                .frame(width: 10, height: 10)
                .foregroundColor(alert.statusColor)
            
            Text(alert.text)
                .font(.custom("Roboto", size: 13))
        }
    }
}

struct AlertListView_Previews: PreviewProvider {
    
    static let alerts = MockAlertService.alerts
    
    static var previews: some View {
        AlertListView(alerts: alerts)
    }
}
