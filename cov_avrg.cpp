/****************** Program introduction **********************
# Calculate covariance using the following equation
# C_{ij}=\frac{\sum_M(\vec{a}_{iM}\cdot\vec{a}_{jM})/\lambda_M}
#	{\sqrt{[\sum_M(\vec{a}_{iM}\cdot\vec{a}_{iM})/\lambda_M]
#	[\sum_M(\vec{a}_{jM}\cdot\vec{a}_{jM})/\lambda_M]}}
#
#                         Author: Qi Wang (wang2qi@mail.uc.edu)
**************************************************************/

/********** Example of input file: input-cutoff10.conf ********
# Data source of eigenvectors.
vecfile	eigenvectors_proteinName_stateID_cutoff10.dat
#
# Dimension of each eigenvector.
vecdim	2660
#
# Candinate modes, seperated by space.
modelist 11 22 33 44 55
#
# Name of output file
outfile	cov_avrg_proteinName_stateID_cutoff10.dat
**************************************************************/

/****************** Format of eigenvector file ****************
[mode_id] [mode_eigenvalue] : [x1] [y1] [z1] ... [xn] [yn] [zn]
***************************************************************/

/**************************** Usage ***************************
Compile:
g++ -std=c++11 cov_avrg.cpp -o a.out
Example:
./a.out input-cutoff10.conf
***************************************************************/

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <iomanip>

// Gloabl arrays.
std::vector<double> eigen_vec;	// size = 3N
std::vector<double> product_ii;	// size = N
std::vector<double> product_ij; // size = N*N
// Function and Data type declaration
struct Config {
	unsigned int vec_dim = 0;
	std::string vecfile_name;
	std::string outfile_name;
	std::vector<unsigned int> mode_list;
	bool is_good = false;
};
Config read_config(const std::string& confg_name);
void print_title();
void check_config (const Config& config);
bool calc_eigenvec_avrg (const std::string& vecfile, const unsigned int& vecdim, const std::vector<unsigned int>& mode_list);
bool calc_eigenvec_corr (const std::string& out_name, const unsigned int& vecdim);

int main(int argc, char* argv[]) {
	// 1. Print program info and read configure file.
	print_title();
	if (2!=argc)  {
		std::cout << "ERROR> No input file found!" << std::endl;
		return 1;
	}
	std::string inp_name = argv[1];
	auto config = read_config(inp_name);
	if(!config.is_good) return 1;
	// 2. Check configure file and resize working arrays.
	check_config(config);
	eigen_vec.resize(3*config.vec_dim);
	product_ii.resize(config.vec_dim);
	product_ij.resize(config.vec_dim*config.vec_dim);
	// 3. Calculate average eigenvector weighted by corresponding eigenvalue.
	if(!calc_eigenvec_avrg(config.vecfile_name, config.vec_dim, config.mode_list)) return 1;
	// 4. Calculate correlation of averaged eigenvector and write data.
	if(!calc_eigenvec_corr(config.outfile_name, config.vec_dim)) return 1;

	return 0;
}

Config read_config(const std::string& config_name) {
	Config config;
	std::ifstream config_file (config_name);
	if(!config_file.is_open()) {
		std::cout << "> Configure file not found!" << std::endl;
	} else {
		std::cout << "> Reading configure file from : " << config_name << std::endl;
	}
	/*read configuration*/
	std::string each_line;
	auto is_space = [](char c) {return std::isspace(c);};
	while(std::getline(config_file, each_line)) {
		std::stringstream each_stream(each_line);
		std::string each_entry;
		/*filter out comment lines and empty lines (including lines of spaces)*/
		if("#"==each_line.substr(0,1) || std::all_of(each_line.begin(), each_line.end(), is_space)) 
			continue;
		each_stream >> each_entry;
		if("vecfile"==each_entry) {
			each_stream >> config.vecfile_name;
		} else if ("vecdim"==each_entry) {
			each_stream >> config.vec_dim;
		} else if ("modelist"==each_entry) {
			unsigned int tmp_mode;
			while(each_stream >> tmp_mode) {
				config.mode_list.push_back(tmp_mode);
			}
		} else if ("outfile"==each_entry) {
			each_stream >> config.outfile_name;
		} else {
			std::cout << "X WARNING> Unknown configure entry!" << std::endl;
		}
	}
	/* Sort the mode list in ascending order, just in case user input mdoes are disordered */
	std::sort(config.mode_list.begin(), config.mode_list.end());
	config_file.close();
	config.is_good = true;
	return config;
}

void print_title() {
	std::cout << std::endl 
			  << "-= EZ-AVRG_CORR version 1.0 =-" 
			  << std::endl << std::endl;
}

void check_config (const Config& config) {
	std::cout << "> After reading, the following configure file will be used :" << std::endl
			  << "o Input file for eigenvectors : " << config.vecfile_name << std::endl
			  << "o Dimension of each eigenvector : " << config.vec_dim << std::endl
			  << "o Modes list for analysis : " << std::endl;
	for (auto imode: config.mode_list) std::cout << "   mode #"<< imode << std::endl;
	std::cout << "o Output file of results : " << config.outfile_name << std::endl;
}

bool calc_eigenvec_avrg (const std::string& vecfile_name, const unsigned int& vecdim, 
		const std::vector<unsigned int>& mode_list) {
	std::ifstream inp_file(vecfile_name);
	if(!inp_file.is_open()) {
		std::cout << "X ERROR: Cannot open file: " << vecfile_name << std::endl;
		return false;
	} else {
		std::cout << "> Reading eigenvectors from file: " << vecfile_name << std::endl;
	}
	unsigned int mode_counter = 0;
	std::string each_line;
	while(std::getline(inp_file, each_line)) {
		auto sep_loc = each_line.find_first_of(":");
		std::stringstream head_info_stream(each_line);
		unsigned int mode_id; double mode_eigenvalue;
		head_info_stream >> mode_id >> mode_eigenvalue;
		if(0==mode_id-mode_list[mode_counter++]) {
			// step1. Read a candidate mode.
			std::stringstream each_stream(each_line.substr(sep_loc+1));
			double x, y, z; unsigned int i=0;
			while(each_stream >> x >> y >> z) {
				eigen_vec[i+0] = x; eigen_vec[i+1] = y; eigen_vec[i+2] = z;
				i+=3;
			}
			// step2. Accumulate this mode to overall average.
			for(unsigned int i=0; i<vecdim; i++) {
				product_ii[i] += (eigen_vec[3*i+0]*eigen_vec[3*i+0] + 
								  eigen_vec[3*i+1]*eigen_vec[3*i+1] + 
								  eigen_vec[3*i+2]*eigen_vec[3*i+2]) / mode_eigenvalue;	
				for (unsigned int j=0; j<vecdim; j++) {
					product_ij[i*vecdim+j] += (eigen_vec[3*i+0]*eigen_vec[3*j+0] + 
											   eigen_vec[3*i+1]*eigen_vec[3*j+1] + 
											   eigen_vec[3*i+2]*eigen_vec[3*j+2]) / mode_eigenvalue;
				}
			}
			std::cout << "> Mode stat: mode #" << mode_id << " with eigenvalue (" << mode_eigenvalue 
			<< ") added to overall average." << std::endl;
		} else {
			mode_counter--;
			continue;
		}
	}
	inp_file.close();
	std::cout << "> Done with eigenvalue-weighted eigenvector" << std::endl;
	return true;
}

bool calc_eigenvec_corr (const std::string& out_name, const unsigned int& vecdim) {
	std::cout << "> Writing output data to file: " << out_name << std::endl;
	std::ofstream out_file(out_name);
	if(!out_file.is_open()) {
		std::cout << "X ERROR: Unable to open file : " << out_name << std::endl;
		return false;
	}
	double cij;
	for(unsigned int i=0; i<vecdim; i++) {
		for(unsigned int j=0; j<vecdim; j++){
			cij = sqrt(product_ii[i]*product_ii[j]);
			cij = product_ij[i*vecdim+j]/cij;
			out_file << std::setw(6) << i+1 << std::setw(6) << j+1 
					 << std::fixed << std::setw(12) << std::setprecision(6) << cij << std::endl;
		}
	}
	out_file.close();
	std::cout << "> Done." << std::endl;
	return true;
}
