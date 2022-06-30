//
//  ErrorView.swift
//  TrustId
//
//  Created by Adamos Adamou on 24/1/22.
//

import SwiftUI

struct ErrorView: View{
    
    @Environment(\.presentationMode) var presentationMode
    
    public let message:String
    
    var body: some View{
        HStack{
            Text(message)
                .font(.custom("Roboto", size: 13))
                .foregroundColor(TrustIdPalette.red)
                .fixedSize(horizontal: false, vertical: true)
            
            Spacer()
            
            Button("Dismiss"){
                presentationMode.wrappedValue.dismiss()
            }
            .font(.custom("Roboto", size: 13))
            .buttonStyle(BlueButton())
        }
        .padding()
        .frame(minWidth:400, maxWidth: 600)
    }
}

struct ErrorView_Previews: PreviewProvider {
    
    static let message = "Any missing, already existing or bad formatted fields will be returned. Any missing, already existing or bad formatted fields will be returned Any missing, already existing or bad formatted fields will be returned"
    
    static var previews: some View {
        ErrorView(message: message)
            .previewLayout(.sizeThatFits)
    }
}
