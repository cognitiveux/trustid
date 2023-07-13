//
//  ExaminationInformationView.swift
//  TrustId
//
//  Created by Adamos Adamou on 1/3/22.
//

import SwiftUI

struct ExaminationInformationView: View {
    
    public let additionalMaterial:Bool
    public let duration:Int
    public let examType:String
    
    var body: some View {
        VStack(alignment: .leading, spacing:2){
            HStack{
                Text("Exam Type: ")
                    .font(.custom("Roboto", size: 13))
                Text(examType)
                    .font(.custom("Roboto", size: 13))
            }
            HStack{
                Text("Exam Duration: ")
                    .font(.custom("Roboto", size: 13))
                Text(duration.description)
                    .font(.custom("Roboto", size: 13))
            }
            HStack{
                Text("Additional Material Allowed: ")
                    .font(.custom("Roboto", size: 13))
                Text(additionalMaterial ? "Yes" : "No" )
                    .font(.custom("Roboto", size: 13))
            }
            Spacer()
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .leading)
        .padding()
    }
}

struct ExaminationInformationView_Previews: PreviewProvider {
    
    static var previews: some View {
        ExaminationInformationView(
            additionalMaterial: true, duration: 50, examType: "Oral"
        )
    }
}
