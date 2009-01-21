/*
 * Contract.java
 *
 */
package com.ib.client;

import java.util.Vector;

public class Contract implements Cloneable {
    
	public int    m_conId;              // contract id, returned from TWS
    public String m_symbol;             // underlying symbol
    public String m_secType;            // security type
    public String m_expiry;             // expiration for futures and options
    public double m_strike;             // strike price for options
    public String m_right;              // put or call (P or C)
    public String m_multiplier;         // multiplier
    public String m_exchange;           // exchange
    public String m_currency;           // currency, e.g. USD
    public String m_localSymbol;        // local symbol for futures or options, e.g. ESZN for ES DEC09 contract 
    public String m_primaryExch;        // for SMART orders, specify an actual exchange where the contract trades, e.g. ISLAND
    public boolean m_includeExpired;    // for contract requests, specifies that even expired contracts should be returned
    
    // COMBOS
    public String m_comboLegsDescrip;   // received in open order version 14 and up for all combos
    public Vector m_comboLegs = new Vector();
    
    // delta neutral
    public UnderComp m_underComp;

    public Contract() {
    	m_conId = 0;
        m_strike = 0;
        m_includeExpired = false;
    }

    public Object clone() throws CloneNotSupportedException {
        Contract retval = (Contract)super.clone();
        retval.m_comboLegs = (Vector)retval.m_comboLegs.clone();
        return retval;
    }

    public Contract(int p_conId, String p_symbol, String p_secType, String p_expiry,
                    double p_strike, String p_right, String p_multiplier,
                    String p_exchange, String p_currency, String p_localSymbol,
                    Vector p_comboLegs, String p_primaryExch, boolean p_includeExpired) {
    	m_conId = p_conId;
        m_symbol = p_symbol;
        m_secType = p_secType;
        m_expiry = p_expiry;
        m_strike = p_strike;
        m_right = p_right;
        m_multiplier = p_multiplier;
        m_exchange = p_exchange;
        m_currency = p_currency;
        m_includeExpired = p_includeExpired;
        m_localSymbol = p_localSymbol;
        m_comboLegs = p_comboLegs;
        m_primaryExch = p_primaryExch;
    }

    public boolean equals(Object p_other) {

    	if (this == p_other) {
    		return true;
    	}

    	if (p_other == null || !(p_other instanceof Contract)) {
    		return false;
    	}

        Contract l_theOther = (Contract)p_other;
        
        if (m_conId != l_theOther.m_conId) {
        	return false;
        }

        if (Util.StringCompare(m_secType, l_theOther.m_secType) != 0) {
        	return false;
        }

        if (Util.StringCompare(m_symbol, l_theOther.m_symbol) != 0 ||
        	Util.StringCompare(m_exchange, l_theOther.m_exchange) != 0 ||
        	Util.StringCompare(m_primaryExch, l_theOther.m_primaryExch) != 0 ||
        	Util.StringCompare(m_currency, l_theOther.m_currency) != 0) {
        	return false;
        }

        if (!Util.NormalizeString(m_secType).equals("BOND")) {

        	if (m_strike != l_theOther.m_strike) {
        		return false;
        	}

        	if (Util.StringCompare(m_expiry, l_theOther.m_expiry) != 0 ||
        		Util.StringCompare(m_right, l_theOther.m_right) != 0 ||
        		Util.StringCompare(m_multiplier, l_theOther.m_multiplier) != 0 ||
        		Util.StringCompare(m_localSymbol, l_theOther.m_localSymbol) != 0) {
        		return false;
        	}
        }

    	// compare combo legs
        if (!Util.VectorEqualsUnordered(m_comboLegs, l_theOther.m_comboLegs)) {
        	return false;
        }
        
        if (m_underComp != l_theOther.m_underComp) {
        	if (m_underComp == null || l_theOther.m_underComp == null) {
        		return false;
        	}
        	if (!m_underComp.equals(l_theOther.m_underComp)) {
        		return false;
        	}
        }

        return true;
    }
    
    public String toString() {
        return m_symbol;
    }
}