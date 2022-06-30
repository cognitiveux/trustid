//
//  MonitoringView.swift
//  TrustId
//
//  Created by Adamos Adamou on 23/1/22.
//

import SwiftUI

struct MonitoringView:View{
    var body: some View{
        VStack(alignment:.leading, spacing: 32){
            Text("Monitoring")
                .font(.custom("Roboto", size: 13))
                .bold()

            VStack(alignment:.leading, spacing:4){
                Text("Camera capture is enabled")
                    .font(.custom("Roboto", size: 13))
                    .foregroundColor(TrustIdPalette.green)
                Text("Checkup running applications is enabled")
                    .font(.custom("Roboto", size: 13))
                    .foregroundColor(TrustIdPalette.green)
            }
            
            Text("TRUSTID will periodically capture your photo for continuous identification purposes and will checkup the running applications and processes on your computer")
                .font(.custom("Roboto", size: 13))
        }
        .background(Color.white)
        .padding()
    }
}

struct MonitoringView_Previews: PreviewProvider {
    static var previews: some View {
        MonitoringView()
    }
}
