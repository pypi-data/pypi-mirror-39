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
//  Command name         |  Method name
//================================================================
//  State                |  Inherited (no method)
//  Status               |  Inherited (no method)
//  cmd_push_pipe_event  |  cmd_push_pipe_event
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
        for (auto i=0; i<pipe.get_data_elt_nb(); i++) {
        	cout << "name " << pipe.get_data_elt_name(i) << endl;
        }
		for (auto i = 0; i < pipe.get_data_elt_nb(); i++) {
			cout << "name " << pipe.get_data_elt_name(i) << endl;
			int data_type = pipe.get_data_elt_type(i);
			cout << "data_type " << data_type << endl;
			if (data_type == Tango::DEV_DOUBLE) {
				Tango::DataElement<double> data;
				pipe >> data;
				cout << "value " << data.value << endl;
			} else if (data_type == Tango::DEV_BOOLEAN) {
				Tango::DataElement<bool> data;
				pipe >> data;
				cout << "value " << data.value << endl;
			} else if (data_type == Tango::DEV_STRING) {
				Tango::DataElement<std::string> data;
				pipe >> data;
				cout << "value " << data.value << endl;
			} else if (data_type == Tango::DEV_LONG64) {
				Tango::DataElement<int64_t> data;
				pipe >> data;
				cout << "value " << data.value << endl;
			} else if (data_type == Tango::DEV_STATE) {
				Tango::DataElement<Tango::DevState> data;
				pipe >> data;
				cout << "value " << data.value << endl;
			} else if (data_type == Tango::DEVVAR_DOUBLEARRAY) {
				std::vector<double> data;
				pipe >> data;
				for (std::vector<double>::iterator it = data.begin() ; it != data.end(); ++it)
					cout << *it << " ";
				cout << endl;
			} else if (data_type == Tango::DEVVAR_LONG64ARRAY) {
				std::vector<int64_t> data;
				pipe >> data;
				for (std::vector<int64_t>::iterator it = data.begin() ; it != data.end(); ++it)
					cout << *it << " ";
				cout << endl;
			} else if (data_type == Tango::DEVVAR_STATEARRAY) {
				std::vector<Tango::DevState> data;
				pipe >> data;
				for (std::vector<Tango::DevState>::iterator it = data.begin() ; it != data.end(); ++it)
					cout << *it << " ";
				cout << endl;
			} else if (data_type == Tango::DEVVAR_STRINGARRAY) {
				std::vector<std::string> data;
				pipe >> data;
				for (std::vector<std::string>::iterator it = data.begin() ; it != data.end(); ++it)
					cout << *it << " ";
				cout << endl;
			} else if (data_type == Tango::DEVVAR_BOOLEANARRAY) {
				std::vector<bool> data;
				pipe >> data;
				for (std::vector<bool>::iterator it = data.begin() ; it != data.end(); ++it)
					cout << *it << " ";
				cout << endl;
			}
		}
	}
	catch (exception &e) {
		cout << "Exception: " << e.what() << endl;
	}
	//	Add your own code here

	/*----- PROTECTED REGION END -----*/	//	PipeServer::write_TestPipe
}
//--------------------------------------------------------
/**
 *	Command cmd_push_pipe_event related method
 *	Description:
 *
 *	@param argin 
 */
//--------------------------------------------------------
void PipeServer::cmd_push_pipe_event(Tango::DevShort argin)
{
	DEBUG_STREAM << "PipeServer::cmd_push_pipe_event()  - " << device_name << endl;
	/*----- PROTECTED REGION ID(PipeServer::cmd_push_pipe_event) ENABLED START -----*/

    if (argin == 0)
	{
		Tango::DevicePipeBlob dpb("PipeEventCase0");

		vector<string> de_inner_inner_names;
		de_inner_inner_names.push_back("InnerInnerFirstDE");
		de_inner_inner_names.push_back("InneraaaaaaaInnerSecondDE");
		inner_inner_blob.set_data_elt_names(de_inner_inner_names);
		inner_inner_blob.set_name("InnerInner");

		dl = 111;
		v_db.clear();
		v_db.push_back(3.33);
		v_db.push_back(3.33);

		inner_inner_blob["InneraaaaaaaInnerSecondDE"] << v_db;
		inner_inner_blob["InnerInnerFirstDE"] << dl;

		vector<string> de_inner_names;
		de_inner_names.push_back("InnerFirstDE");
		de_inner_names.push_back("InnerSecondDE");
		de_inner_names.push_back("InnerThirdDE");
		inner_blob.set_data_elt_names(de_inner_names);
		inner_blob.set_name("Inner");

		inner_str = "Grenoble";
		inner_bool = true;

		inner_blob << inner_str << inner_inner_blob << inner_bool;

		vector<string> de_names;
		de_names.push_back("1DE");
		de_names.push_back("2DE");
		dpb.set_data_elt_names(de_names);

		v_dl.clear();
		v_dl.push_back(3);
		v_dl.push_back(4);
		v_dl.push_back(5);
		v_dl.push_back(6);

		dpb << inner_blob << v_dl;
		this->push_pipe_event("TestPipe",&dpb);
	}
	else if (argin == 1)
	{
		Tango::DevicePipeBlob dpb("PipeEventCase1");
		vector<string> de_names;
		de_names.push_back("Another_1DE");
		de_names.push_back("Another_2DE");
		dpb.set_data_elt_names(de_names);

		v_dl.clear();
		v_dl.push_back(2);
		string str("Barcelona");

		dpb << v_dl << str;

		this->push_pipe_event("TestPipe",&dpb);
	}
	else if (argin == 2)
	{
		Tango::DevicePipeBlob dpb("PipeEventCase2");
		vector<string> de_names;
		de_names.push_back("Qwerty_1DE");
		de_names.push_back("Azerty_2DE");
		dpb.set_data_elt_names(de_names);

		std::vector<Tango::DevFloat> v_df;
		v_df.clear();
		v_df.push_back(3.142);
		v_df.push_back(6.284);
		v_df.push_back(12.568);
		v_df.push_back(25.136);
		string str("Barcelona");

		dpb << str << v_df;

#ifdef WIN32
		struct _timeb tv;
		tv.time = 10;
		tv.millitm = 0;
		this->push_pipe_event("TestPipe",&dpb,tv);
#else
		struct timeval tv;
		tv.tv_sec = 10;
		tv.tv_usec = 0;
		this->push_pipe_event("TestPipe",&dpb,tv);
#endif
	}
	else if (argin == 3)
	{
		Tango::DevErrorList del;
		del.length(1);
		del[0].reason = CORBA::string_dup("aaa");
		del[0].desc = CORBA::string_dup("bbb");
		del[0].origin = CORBA::string_dup("ccc");
		Tango::DevFailed df(del);
		this->push_pipe_event("TestPipe",&df);
	}
	else if (argin == 4)
	{
		Tango::DevicePipeBlob dpb("PipeEventCase4");
		vector<string> de_names;
		de_names.push_back("Lunes");
		de_names.push_back("Martes");
		dpb.set_data_elt_names(de_names);

		string str("Girona");

		v_dl.clear();
		for (int loop = 0;loop < 3000;loop++)
			v_dl.push_back(loop);

		dpb << str << v_dl;

		this->push_pipe_event("TestPipe",&dpb);
	}

	/*----- PROTECTED REGION END -----*/	//	PipeServer::cmd_push_pipe_event
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

//	Additional Methods

/*----- PROTECTED REGION END -----*/	//	PipeServer::namespace_ending
} //	namespace
