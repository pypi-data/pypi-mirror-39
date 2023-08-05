/*----- PROTECTED REGION ID(PipeServer.cpp) ENABLED START -----*/
static const char *RcsId = "$Id:  $";
//=============================================================================
//
// file :        PipeServer.cpp
//
// description : C++ source for the PipeServer class and its commands.
//               The class is derived from Device. It represents the
//               CORBA servant object which will be accessed from the
//               network. All commands which can be executed on the
//               PipeServer are implemented in this file.
//
// project :     
//
// This file is part of Tango device class.
// 
// Tango is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// Tango is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with Tango.  If not, see <http://www.gnu.org/licenses/>.
// 
// $Author:  $
//
// $Revision:  $
// $Date:  $
//
// $HeadURL:  $
//
//=============================================================================
//                This file is generated by POGO
//        (Program Obviously used to Generate tango Object)
//=============================================================================


#include <PipeServer.h>
#include <PipeServerClass.h>

/*----- PROTECTED REGION END -----*/	//	PipeServer.cpp

/**
 *  PipeServer class description:
 *    
 */

//================================================================
//  The following table gives the correspondence
//  between command and method names.
//
//  Command name  |  Method name
//================================================================
//  State         |  Inherited (no method)
//  Status        |  Inherited (no method)
//================================================================

//================================================================
//  Attributes managed is:
//================================================================
//================================================================

namespace PipeServer_ns
{
/*----- PROTECTED REGION ID(PipeServer::namespace_starting) ENABLED START -----*/

//	static initializations

/*----- PROTECTED REGION END -----*/	//	PipeServer::namespace_starting

//--------------------------------------------------------
/**
 *	Method      : PipeServer::PipeServer()
 *	Description : Constructors for a Tango device
 *                implementing the classPipeServer
 */
//--------------------------------------------------------
PipeServer::PipeServer(Tango::DeviceClass *cl, string &s)
 : TANGO_BASE_CLASS(cl, s.c_str())
{
	/*----- PROTECTED REGION ID(PipeServer::constructor_1) ENABLED START -----*/
	init_device();
	
	/*----- PROTECTED REGION END -----*/	//	PipeServer::constructor_1
}
//--------------------------------------------------------
PipeServer::PipeServer(Tango::DeviceClass *cl, const char *s)
 : TANGO_BASE_CLASS(cl, s)
{
	/*----- PROTECTED REGION ID(PipeServer::constructor_2) ENABLED START -----*/
	init_device();
	
	/*----- PROTECTED REGION END -----*/	//	PipeServer::constructor_2
}
//--------------------------------------------------------
PipeServer::PipeServer(Tango::DeviceClass *cl, const char *s, const char *d)
 : TANGO_BASE_CLASS(cl, s, d)
{
	/*----- PROTECTED REGION ID(PipeServer::constructor_3) ENABLED START -----*/
	init_device();
	
	/*----- PROTECTED REGION END -----*/	//	PipeServer::constructor_3
}

//--------------------------------------------------------
/**
 *	Method      : PipeServer::delete_device()
 *	Description : will be called at device destruction or at init command
 */
//--------------------------------------------------------
void PipeServer::delete_device()
{
	DEBUG_STREAM << "PipeServer::delete_device() " << device_name << endl;
	/*----- PROTECTED REGION ID(PipeServer::delete_device) ENABLED START -----*/
	
	//	Delete device allocated objects
	
	/*----- PROTECTED REGION END -----*/	//	PipeServer::delete_device
}

//--------------------------------------------------------
/**
 *	Method      : PipeServer::init_device()
 *	Description : will be called at device initialization.
 */
//--------------------------------------------------------
void PipeServer::init_device()
{
	DEBUG_STREAM << "PipeServer::init_device() create device " << device_name << endl;
	/*----- PROTECTED REGION ID(PipeServer::init_device_before) ENABLED START -----*/
	
	//	Initialization before get_device_property() call
	
	/*----- PROTECTED REGION END -----*/	//	PipeServer::init_device_before
	//	No device property to be read from database
	
	/*----- PROTECTED REGION ID(PipeServer::init_device) ENABLED START -----*/
	
	//	Initialize device

	/*----- PROTECTED REGION END -----*/	//	PipeServer::init_device
}


//--------------------------------------------------------
/**
 *	Method      : PipeServer::always_executed_hook()
 *	Description : method always executed before any command is executed
 */
//--------------------------------------------------------
void PipeServer::always_executed_hook()
{
	DEBUG_STREAM << "PipeServer::always_executed_hook()  " << device_name << endl;
	/*----- PROTECTED REGION ID(PipeServer::always_executed_hook) ENABLED START -----*/
	
	//	code always executed before all requests
	
	/*----- PROTECTED REGION END -----*/	//	PipeServer::always_executed_hook
}

//--------------------------------------------------------
/**
 *	Method      : PipeServer::read_attr_hardware()
 *	Description : Hardware acquisition for attributes
 */
//--------------------------------------------------------
void PipeServer::read_attr_hardware(TANGO_UNUSED(vector<long> &attr_list))
{
	DEBUG_STREAM << "PipeServer::read_attr_hardware(vector<long> &attr_list) entering... " << endl;
	/*----- PROTECTED REGION ID(PipeServer::read_attr_hardware) ENABLED START -----*/
	
	//	Add your own code
	
	/*----- PROTECTED REGION END -----*/	//	PipeServer::read_attr_hardware
}


//--------------------------------------------------------
/**
 *	Method      : PipeServer::add_dynamic_attributes()
 *	Description : Create the dynamic attributes if any
 *                for specified device.
 */
//--------------------------------------------------------
void PipeServer::add_dynamic_attributes()
{
	/*----- PROTECTED REGION ID(PipeServer::add_dynamic_attributes) ENABLED START -----*/
	
	//	Add your own code to create and add dynamic attributes if any
	
	/*----- PROTECTED REGION END -----*/	//	PipeServer::add_dynamic_attributes
}

//--------------------------------------------------------
/**
 *	Read pipe TestPipe related method
 *	Description: 
 */
//--------------------------------------------------------
void PipeServer::read_TestPipe(Tango::Pipe &pipe)
{
	DEBUG_STREAM << "PipeServer::read_TestPipe(Tango::Pipe &pipe) entering... " << endl;
	/*----- PROTECTED REGION ID(PipeServer::read_TestPipe) ENABLED START -----*/
	
    vector<string> de_names;
    de_names.push_back("x");
    de_names.push_back("y");
    de_names.push_back("width");
    de_names.push_back("height");
    pipe.set_data_elt_names(de_names);

    Tango::DevFloat y,width,height;
    Tango::DevFloat x = 5.9;
    y=6.0;
    width=30.0;
    height=45.0;
    string root_name = "theBlob";

    pipe.set_root_blob_name(root_name);
    pipe << x << y << width << height;
	
	/*----- PROTECTED REGION END -----*/	//	PipeServer::read_TestPipe
}
//--------------------------------------------------------
/**
 *	Write pipe TestPipe related method
 *	Description: 
 */
//--------------------------------------------------------
void PipeServer::write_TestPipe(Tango::WPipe &pipe)
{
	DEBUG_STREAM << "PipeServer::write_TestPipe(Tango::WPipe &pipe) entering... " << endl;
	/*----- PROTECTED REGION ID(PipeServer::write_TestPipe) ENABLED START -----*/
    cout << "root blob name " << pipe.get_root_blob_name() << endl;
    cout << "nb of data elements " << pipe.get_data_elt_nb() << endl;
    try {
    	extract(pipe);
    }
    catch (exception &e) {
    	cout << "Exception: " << e.what() << endl;
    }
	//	Add your own code here
	
	/*----- PROTECTED REGION END -----*/	//	PipeServer::write_TestPipe
}
//--------------------------------------------------------
/**
 *	Method      : PipeServer::add_dynamic_commands()
 *	Description : Create the dynamic commands if any
 *                for specified device.
 */
//--------------------------------------------------------
void PipeServer::add_dynamic_commands()
{
	/*----- PROTECTED REGION ID(PipeServer::add_dynamic_commands) ENABLED START -----*/
	
	//	Add your own code to create and add dynamic commands if any
	
	/*----- PROTECTED REGION END -----*/	//	PipeServer::add_dynamic_commands
}

/*----- PROTECTED REGION ID(PipeServer::namespace_ending) ENABLED START -----*/

template<typename T>
void PipeServer::extract(T& obj) {
	for (unsigned i = 0; i < obj.get_data_elt_nb(); i++) {
		cout << "name " << obj.get_data_elt_name(i) << endl;
	}
	for (unsigned i = 0; i < obj.get_data_elt_nb(); i++) {
		cout << "name " << obj.get_data_elt_name(i) << endl;
		int data_type = obj.get_data_elt_type(i);
		cout << "data_type " << data_type << endl;
		if (data_type == Tango::DEV_DOUBLE) {
			Tango::DataElement<double> data;
			obj >> data;
			cout << "value " << data.value << endl;
		} else if (data_type == Tango::DEV_BOOLEAN) {
			Tango::DataElement<bool> data;
			obj >> data;
			cout << "value " << data.value << endl;
		} else if (data_type == Tango::DEV_STRING) {
			Tango::DataElement < std::string > data;
			obj >> data;
			cout << "value " << data.value << endl;
		} else if (data_type == Tango::DEV_LONG64) {
			Tango::DataElement < int64_t > data;
			obj >> data;
			cout << "value " << data.value << endl;
		} else if (data_type == Tango::DEV_STATE) {
			Tango::DataElement < Tango::DevState > data;
			obj >> data;
			cout << "value " << data.value << endl;
		} else if (data_type == Tango::DEVVAR_DOUBLEARRAY) {
			std::vector<double> data;
			obj >> data;
			for (std::vector<double>::iterator it = data.begin(); it != data.end(); ++it)
				cout << *it << " ";
			cout << endl;
		} else if (data_type == Tango::DEVVAR_LONG64ARRAY) {
			std::vector < int64_t > data;
			obj >> data;
			for (std::vector<int64_t>::iterator it = data.begin(); it != data.end(); ++it)
				cout << *it << " ";
			cout << endl;
		} else if (data_type == Tango::DEVVAR_STATEARRAY) {
			std::vector < Tango::DevState > data;
			obj >> data;
			for (std::vector<Tango::DevState>::iterator it = data.begin(); it != data.end(); ++it)
				cout << *it << " ";
			cout << endl;
		} else if (data_type == Tango::DEVVAR_STRINGARRAY) {
			std::vector < std::string > data;
			obj >> data;
			for (std::vector<std::string>::iterator it = data.begin(); it != data.end(); ++it)
				cout << *it << " ";
			cout << endl;
		} else if (data_type == Tango::DEVVAR_BOOLEANARRAY) {
			std::vector<bool> data;
			obj >> data;
			for (std::vector<bool>::iterator it = data.begin(); it != data.end(); ++it)
				cout << *it << " ";
			cout << endl;
		} else if (data_type == Tango::DEV_PIPE_BLOB) {
			cout << "Found inner blob" << endl;
			Tango::DevicePipeBlob blob;
			obj >> blob;
			extract (blob);
		}
	}
}
		//	Additional Methods

/*----- PROTECTED REGION END -----*/	//	PipeServer::namespace_ending
} //	namespace
