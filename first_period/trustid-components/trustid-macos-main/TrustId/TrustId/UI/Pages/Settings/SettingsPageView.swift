//
//  SettingsPageView.swift
//  TrustId
//
//  Created by Adamos Adamou on 6/12/21.
//

import SwiftUI

struct SettingsPageView: View {
    var body: some View {
        VStack {
            Text("SettingsPageView")
                .font(.custom("Roboto", size: 13))
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color.white)
        .addNavigationHeader()
    }
}

struct SettingsPageView_Previews: PreviewProvider {
    static var previews: some View {
        SettingsPageView()
    }
}
