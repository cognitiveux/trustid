//
//  StudentIdentificationLayout.swift
//  TrustId
//
//  Created by Adamos Adamou on 28/12/21.
//

import SwiftUI

struct StudentIdentificationLayout<CameraContent:View, StatusContent:View, ActionContent:View>: View {
    
    public let cameraContent: () -> CameraContent
    public let statusContent: () -> StatusContent
    public let actionContent: () -> ActionContent
    
    var body: some View {
        GeometryReader{ proxy in
            HStack{
                VStack{
                    cameraContent()
                        .frame(height:proxy.size.height*0.74)
                    Divider()
                    actionContent()
                        .frame(height:proxy.size.height*0.25)
                }
                Divider()
                statusContent()
                    .frame(width:proxy.size.width*0.25)
            }
        }
    }
}

struct StudentIdentificationLayout_Previews: PreviewProvider {
    static var previews: some View {
        StudentIdentificationLayout {
            Color.black
        } statusContent: {
            Color.blue
        } actionContent: {
            Color.gray
        }
    }
}
