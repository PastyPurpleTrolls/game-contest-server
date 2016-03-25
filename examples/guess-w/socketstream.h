#pragma once
#ifndef _SOCKETSTREAM_H
#define _SOCKETSTREAM_H

// downloaded from http://www.cplusplus.com/forum/general/58677/

/*-----------------------------------------------------------------.
| Copyright (C) 2011 Galik grafterman@googlemail.com               |
'------------------------------------------------------------------'

This code is was created from code (C) Copyright Nicolai M. Josuttis 2001
with the following Copyright Notice:
*/

/* The following code declares classes to read from and write to
 * file descriptore or file handles.
 *
 * See
 *      http://www.josuttis.com/cppcode
 * for details and the latest version.
 *
 * - open:
 *      - integrating BUFSIZ on some systems?
 *      - optimized reading of multiple characters
 *      - stream for reading AND writing
 *      - i18n
 *
 * (C) Copyright Nicolai M. Josuttis 2001.
 * Permission to copy, use, modify, sell and distribute this software
 * is granted provided this copyright notice appears in all copies.
 * This software is provided "as is" without express or implied
 * warranty, and with no claim as to its suitability for any purpose.
 *
 * Version: Jul 28, 2002
 * History:
 *  Jul 28, 2002: bugfix memcpy() => memmove()
 *                fdinbuf::underflow(): cast for return statements
 *  Aug 05, 2001: first public version
 */

 /*

Permission to copy, use, modify, sell and distribute this software
is granted under the same conditions.

'----------------------------------------------------------------*/

extern "C" {
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <errno.h>
}
#include <exception>
#include <streambuf>
#include <istream>
#include <ostream>
#include <iostream>

namespace net {

template<typename Char>
class basic_socketbuf
: public std::basic_streambuf<Char>
{
public:
	typedef Char char_type;
	typedef std::basic_streambuf<char_type> buf_type;
	typedef std::basic_ostream<char_type> stream_type;
	typedef typename buf_type::int_type int_type;
	typedef typename std::basic_streambuf<Char>::traits_type traits_type;

protected:

	static const int char_size = sizeof(char_type);
	static const int SIZE = 128;
	char_type obuf[SIZE] ;
	char_type ibuf[SIZE] ;

	int sock;

public:
	basic_socketbuf(): sock(0)
	{
		buf_type::setp(obuf, obuf + (SIZE - 1));
		buf_type::setg(ibuf, ibuf, ibuf);
	}

	virtual ~basic_socketbuf() { sync(); }

	void set_socket(int sock) { this->sock = sock; }
	int get_socket() { return this->sock; }

protected:

	int output_buffer()
	{
		int num = buf_type::pptr() - buf_type::pbase();
		if(send(sock, reinterpret_cast<char*>(obuf), num * char_size, 0) != num)
			return traits_type::eof();
		buf_type::pbump(-num);
		return num;
	}

	virtual int_type overflow(int_type c)
	{
		if(c != traits_type::eof())
		{
			*buf_type::pptr() = c;
			buf_type::pbump(1);
		}

		if(output_buffer() == traits_type::eof())
			return traits_type::eof();
		return c;
	}

	virtual int sync()
	{
		if(output_buffer() == traits_type::eof())
			return traits_type::eof();
		return 0;
	}

	virtual int_type underflow()
	{
		if(buf_type::gptr() < buf_type::egptr())
			return *buf_type::gptr();

		int num;
		if((num = recv(sock, reinterpret_cast<char*>(ibuf), SIZE * char_size, 0)) <= 0)
			return traits_type::eof();

		buf_type::setg(ibuf, ibuf, ibuf + num);
		return *buf_type::gptr();
	}
};

typedef basic_socketbuf<char> socketbuf;
typedef basic_socketbuf<wchar_t> wsocketbuf;

template<typename Char>
class basic_socketstream
: public std::basic_iostream<Char>
{
public:
	typedef Char char_type;
	typedef std::basic_iostream<char_type> stream_type;
	typedef basic_socketbuf<char_type> buf_type;

protected:
	buf_type buf;

public:
	basic_socketstream(): stream_type(&buf) {}
	basic_socketstream(int s): stream_type(&buf) { buf.set_socket(s); }
	basic_socketstream(const std::string& host, uint16_t port)
	    : stream_type(&buf)
	{
	    if (!open(host, port)) {
		throw std::runtime_error("connect() failed") ;
	    }
	}

	void close() {
		if(buf.get_socket() != 0) ::close(buf.get_socket());
		stream_type::clear();
	}

	bool open(const std::string& host, const uint16_t port) {
		close();
		int sd = socket(AF_INET, SOCK_STREAM, 0);
		sockaddr_in sin;
		hostent *he = gethostbyname(host.c_str());

		std::copy(reinterpret_cast<char*>(he->h_addr)
			, reinterpret_cast<char*>(he->h_addr) + he->h_length
			, reinterpret_cast<char*>(&sin.sin_addr.s_addr));
		sin.sin_family = AF_INET;
		sin.sin_port = htons(port);

		if(connect(sd, reinterpret_cast<sockaddr*>(&sin), sizeof(sin)) < 0) {
			stream_type::setstate(std::ios::failbit);
			return false;
		}

		buf.set_socket(sd);
		return true;
	}
};

typedef basic_socketstream<char> socketstream;
typedef basic_socketstream<wchar_t> wsocketstream;

template<typename Char>
class basic_server {
    private:
        int sd;
	int port;

    public:
	~basic_server() { close(sd); }

        basic_server(uint16_t use_port = 0) : port(use_port) {
		sd = socket(AF_INET, SOCK_STREAM, 0);
		if (sd < 0) {
			throw std::runtime_error("socket() failed") ;
		}

		sockaddr_in server;
		server.sin_family = AF_INET;
		server.sin_addr.s_addr = INADDR_ANY;
		server.sin_port = htons(port);

		if (bind(sd, reinterpret_cast<sockaddr*>(&server), sizeof(server)) < 0) {
			throw std::runtime_error("bind() failed");
		}

		socklen_t slen = sizeof(server);
		if (getsockname(sd, reinterpret_cast<sockaddr*>(&server), &slen) < 0) {
			throw std::runtime_error("getsockname() failed");
		}

		port = ntohs(server.sin_port);

		if (listen(sd, 5) < 0) {
			throw std::runtime_error("listen() failed");
		}
	}

	basic_socketstream<Char>* serve() const {
		int cd = accept(sd, NULL, NULL);
		if (cd < 0) {
			throw std::runtime_error("accept() failed");
		}

		return new basic_socketstream<Char>(cd);
	}

	int get_port() const { return port; }
};

typedef basic_server<char> server;
typedef basic_server<wchar_t> wserver;

} // net namespace

#endif // _SOCKETSTREAM_H
